from typing import List
from app.repositories import VideoRepository
from app.models import MediaInfo, User, Video
from app.dtos import VideoDTO
from app.exceptions import HandledException
from app.integrations import AIGenerator, CloudinaryClient

class GeneratorService:
    @staticmethod
    async def get_suggested_topics(keyword: str, limit: int) -> List[str]:
        # Generate topic suggestions (based on a keyword).
        return await AIGenerator.generate_topic_suggestions(keyword, limit)

    @staticmethod
    async def get_trending_topics(limit: int) -> List[str]:
        # Generate trending topics.
        return await AIGenerator.generate_trending_topics(limit)

    @staticmethod
    async def generate_script(topic: str, creator: User) -> VideoDTO:
        # Generate a script based on the topic.
        if not topic:
            raise HandledException("Topic must not empty", 400)
        
        script = await AIGenerator.generate_script(topic)

        # Create a draft video entry with the generated script.
        data = {
            "topic": topic,
            "script": script,
            "creator": creator,
            "status": "draft"
        }
        video = VideoRepository.create_video(data)

        return VideoDTO.from_model(video)
    
    @staticmethod
    async def regenerate_script(video_id: str) -> VideoDTO:
        # Regenerate script for an existing video.
        video = VideoRepository.find_by_id(video_id)
        if not video:
            raise HandledException("Video does not exist", 404)
        
        # Generate a new script based on the existing topic.
        new_script = await AIGenerator.generate_script(video.topic)

        # Update the video with the new script.
        video = VideoRepository.update_script(video, new_script)

        return VideoDTO.from_model(video)

    @staticmethod
    async def generate_voice(video_id: str, script: str, creator: User) -> VideoDTO:
        video = VideoRepository.find_by_id(video_id)
        if not video:
            raise HandledException("Video does not exist", 404)
        if str(video.creator.id) != str(creator.id):
            raise HandledException("Permission denied", 403)
        if not script:
            raise HandledException("Script must not empty", 400)

        # Generate voice audio from script and create a draft video entry.
        audio_bytes = await AIGenerator.generate_voice(script)

        # Upload generated audio to Cloudinary (as video resource type).
        upload_res = await CloudinaryClient.upload_file(
            data=audio_bytes,
            resource_type="video",  # Cloudinary treats mp3 as video
            folder=f"{creator.id}/voices"
        )
        
        video = VideoRepository.update_voice(
            video=video,
            public_id=upload_res["public_id"],
            url=upload_res["url"],
            format=upload_res["format"],
            size=upload_res["bytes"]
        )

        # Return the created video as a DTO.
        return VideoDTO.from_model(video)

    @staticmethod
    async def generate_video(video_id: str, creator_id: str) -> VideoDTO:
        # Generate a video
        video = VideoRepository.find_by_id(video_id)
        if not video:
            raise HandledException("Video does not exist", 404)
        if str(video.creator.id) != creator_id:
            raise HandledException("Permission denied", 403)
        if not video.voice_file:
            raise HandledException("Voice does not exist", 400)
        
        # TODO: Upload the generated video to Cloudinary
        video_bytes = await AIGenerator.generate_video(video)
        # public_id, video_url = await CloudinaryClient.upload_bytes(
        #     data=video_bytes,
        #     resource_type="video",
        #     folder=f"{creator_id}/videos"
        # )

        public_id = "mock_video_id"
        video_url = "https://res.cloudinary.com/df8meqyyc/video/upload/v1750280402/text-to-video_rmp4vx.mp4"
        
        video = VideoRepository.update_video(video, public_id, video_url)
        VideoRepository.update_status(video, "done")
        
        return VideoDTO.from_model(video)