import replicate
from app.exceptions import HandledException
from config import settings

class StableDiffusionClient:

    @staticmethod
    def generate_image(label: str) -> str:
        try:
            return "https://picsum.photos/640/360"
            output = replicate.run(
                settings.STABILITY_MODEL_ID,
                input={
                    "prompt": label,
                    "num_outputs": 1
                },
                api_token=settings.REPLICATE_API_TOKEN
            )

            # Trả về URL ảnh đầu tiên (có thể thêm logic random, multiple, ...)
            image_url = output[0].url if hasattr(output[0], "url") else str(output[0])
            return image_url

        except Exception as e:
            raise HandledException(
                status_code=500,
                detail=f"Image generation failed: {str(e)}"
            )
