import asyncio
from httpx import ReadTimeout
from replicate import async_run
from replicate.exceptions import ModelError
from config import settings

class StableDiffusionClient:
    @staticmethod
    async def generate_image(label: str) -> str:
        # Trả về ảnh demo
        return "https://picsum.photos/640/360"

        try:
            output = await async_run(
                settings.STABILITY_MODEL_ID,
                input={"prompt": label, "num_outputs": 1},
                api_token=settings.REPLICATE_API_TOKEN
            )
        except ReadTimeout as e:
            raise RuntimeError("Replicate connection timed out.") from e
        except ModelError as e:
            raise ValueError("Image model failed to generate result.") from e
        except Exception as e:
            raise RuntimeError("Failed to generate image from prompt.") from e

        if not output:
            raise ValueError("No image generated from prompt.")
        try:
            return output[0].url
        except Exception as e:
            raise RuntimeError("No image URL in result.") from e

    @staticmethod
    async def generate_images(labels: list[str]) -> list[str]:
        """Return videos url"""
        # Coroutine object: 
        tasks = [StableDiffusionClient.generate_image(label) for label in labels]
        return await asyncio.gather(*tasks)