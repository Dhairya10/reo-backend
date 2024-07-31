import time
import openai
from fastapi import HTTPException
from supabase import Client
from models.stories import GeneratedStoryCreate, GeneratedStory
from config.logger import logger
from typing import List
import os

class StoryService:
    def __init__(self, supabase: Client):
        self.supabase = supabase

    def generate_story(self, topic, characters, duration):
        characters_str = ", ".join(characters)
        prompt = f"""Write a short, kid-friendly story about {topic} featuring the following characters: {characters_str}. Start the story with a fun title. The story should be {duration} minutes long. Make sure the story is engaging, fun, and appropriate for pre-schoolers, incorporating all the selected characters in a meaningful way.
        Think before you write the story. First, consider the age group of pre-schoolers and what themes, language, and story structures would be most appropriate and engaging for them. Then, reflect on how each of the selected characters can be meaningfully integrated into the story about the given topic, ensuring each character has a purpose and contributes to the narrative. Consider how the topic can be explored in a way that is both educational and entertaining for young children. Finally, plan the story arc to include a clear beginning, middle, and end, with a simple but valuable lesson or takeaway appropriate for pre-schoolers. After this careful consideration, write the short, kid-friendly story, keeping it within {duration} minutes and maintaining an engaging, fun, and age-appropriate tone throughout.
        DO NOT OUTPUT INFORMATION LIKE WORD COUNT, THE ENDING, OR ANYTHING ELSE. JUST WRITE THE STORY.
        """

        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates kid-friendly stories."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=5000
        )
        generated_story = response.choices[0].message.content

        return generated_story

    def get_audio_file(self, text, user_id):
        response = openai.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text,
        )

        # Generate a unique filename using a timestamp
        filename = f"output_{int(time.time())}.mp3"
        
        # Write the file temporarily
        response.write_to_file(filename)

        try:
            # Upload the file to Supabase storage
            with open(filename, 'rb') as f:
                res = self.supabase.storage.from_('audio_files').upload(
                    file=f,
                    path=f"{user_id}/{filename}",
                    file_options={"content-type": "audio/mpeg"}
                )

            # Get the public URL
            public_url = self.supabase.storage.from_('audio_files').get_public_url(f"{user_id}/{filename}")

            # Remove the temporary file
            os.remove(filename)

            return public_url

        except Exception as e:
            logger.error(f"Error uploading audio file to Supabase: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to upload audio file")


    async def create_story(self, story: GeneratedStoryCreate, user_id: str) -> GeneratedStory:
        try:
            # Generate the story text
            story_text = self.generate_story(story.topic, story.characters, story.duration)
            
            # Generate the audio file and get its public URL
            audio_url = self.get_audio_file(story_text, user_id)
            
            # Prepare data for database insertion
            story_data = {
                "user_id": user_id,
                "topic": story.topic,
                "characters": story.characters,
                "duration": story.duration,
                "story_text": story_text,
                "audio_url": audio_url
            }
            
            # Insert into database
            response = self.supabase.table("generated_stories").insert(story_data).execute()
            
            if response.data:
                return GeneratedStory(**response.data[0])
            else:
                raise HTTPException(status_code=500, detail="Failed to create story in database")
        except Exception as e:
            logger.error(f"Error in create_story: {str(e)}")
            raise HTTPException(status_code=500, detail="An error occurred while creating the story")


    async def get_stories(self, user_id: str) -> List[GeneratedStory]:
        try:
            response = self.supabase.table("generated_stories").select("*").eq("user_id", user_id).execute()
            return [GeneratedStory(**story) for story in response.data]
        except Exception as e:
            logger.error(f"Error in get_stories: {str(e)}")
            raise HTTPException(status_code=500, detail="An error occurred while fetching stories")