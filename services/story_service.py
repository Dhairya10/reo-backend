from supabase import Client
from models.stories import GeneratedStoryCreate, GeneratedStory
from config.logger import logger
import uuid

class StoryService:
    def __init__(self, supabase: Client):
        self.supabase = supabase

    async def create_story(self, story: GeneratedStoryCreate, user_id: str) -> GeneratedStory:
        try:
            # Generate the story content (this would involve calling an AI service)
            story_content = await self._generate_story_content(story.topic, story.characters)
            
            # Generate audio from the story content
            audio_file = await self._generate_audio(story_content)
            
            # Upload audio to Supabase Storage
            file_path = f"audio_stories/{uuid.uuid4()}.mp3"
            await self._upload_to_storage(file_path, audio_file)
            
            # Get the public URL of the uploaded file
            audio_url = self.supabase.storage.from_("audio_stories").get_public_url(file_path)
            
            # Create the story record in the database
            story_data = story.dict()
            story_data.update({
                "user_id": user_id,
                "content": story_content,
                "audio_url": audio_url
            })
            
            response = self.supabase.table("generated_stories").insert(story_data).execute()
            created_story = response.data[0]
            
            logger.info(f"Successfully created story with ID {created_story['id']}")
            return GeneratedStory(**created_story)
        except Exception as e:
            logger.error(f"Error creating story: {str(e)}")
            raise

    async def _generate_story_content(self, topic: str, characters: List[str]) -> str:
        # Implementation to generate story content using an AI service
        pass

    async def _generate_audio(self, content: str):
        # Implementation to generate audio from text
        pass

    async def _upload_to_storage(self, file_path: str, file_content):
        # Implementation to upload file to Supabase Storage
        pass