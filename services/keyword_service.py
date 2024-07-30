import openai
from models.keywords import KeywordBase
from utils.auth import get_supabase_vector_db
from config.logger import logger
from config.settings import OPENAI_API_KEY
from supabase import Client


async def generate_embedding(text):
    """
    Generate an embedding for the given text using OpenAI's embedding model.
    
    :param text: The input text to generate an embedding for.
    :return: A list representing the embedding vector.
    """
    openai.api_key = OPENAI_API_KEY
    
    response = openai.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    
    embedding = response.data[0].embedding
    return embedding


async def query_database(db, query_text, limit=5, similarity_threshold=0.75):
    """
    Query the database for similar vectors based on the input text and return only video_ids.
    
    :param db: The SupabaseVectorDB instance.
    :param query_text: The input text to search for similar entries.
    :param limit: The maximum number of results to return (default: 5).
    :param similarity_threshold: The minimum similarity score to include in results (default: 0.75).
    :return: A list of video_ids, sorted by similarity.
    """
    # Generate embedding for the query text
    query_embedding = await generate_embedding(query_text)

    # Query the database
    query_result = db.query_vectors(
        query_vector=query_embedding,
        limit=limit
    )

    # Process the results
    results = []
    for item in query_result:
        video_id = item[0]
        similarity_score = item[1]
        
        # Filter results based on similarity threshold
        if similarity_score >= similarity_threshold:
            results.append((video_id, similarity_score))

    # Sort results by similarity score in descending order
    results.sort(key=lambda x: x[1], reverse=True)

    # Return only the video_ids
    return [video_id for video_id, _ in results]


async def process_keyword(keyword: KeywordBase, user_id: str, supabase: Client):
    try:
        # Initialize the SupabaseVectorDB
        db = await get_supabase_vector_db()

        # Run similarity search
        similar_videos = await query_database(db, keyword.word)

        if similar_videos:
            # Add the keyword to the keywords table
            keyword_response = supabase.table('keywords').insert({
                'word': keyword.word
            }).execute()
            keyword_id = keyword_response.data[0]['id']

            # Add the keyword data to user_blocked_keywords table
            supabase.table('user_blocked_keywords').insert({
                'user_id': user_id,
                'keyword_id': keyword_id
            }).execute()

            # For each video_id returned from the list, add the keyword uuid to videos table
            for video_id in similar_videos:
                supabase.table('videos').update({
                    'keywords': f"array_append(keywords, '{keyword_id}')"
                }).eq('id', video_id).execute()

            logger.info(f"Keyword '{keyword.word}' processed and added for user {user_id}")
            return {
                "success": True,
                "message": f"Keyword '{keyword.word}' processed successfully",
                "keyword_id": keyword_id,
                "affected_videos": len(similar_videos)
            }
        else:
            logger.info(f"No similar videos found for keyword '{keyword.word}' for user {user_id}")
            return {
                "success": True,
                "message": f"No similar videos found for keyword '{keyword.word}'",
                "keyword_id": None,
                "affected_videos": 0
            }

    except Exception as e:
        logger.error(f"Error processing keyword '{keyword.word}' for user {user_id}: {str(e)}")
        return {
            "success": False,
            "message": f"Error processing keyword: {str(e)}",
            "keyword_id": None,
            "affected_videos": 0
        }