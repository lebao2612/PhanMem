import asyncio
import replicate
from httpx import ReadTimeout
from replicate.exceptions import ModelError

class ReplicateClient:
    def __init__(self, model_id: str, api_token: str):
        self.model_id = model_id
        self.api_token = api_token
        self.client = replicate.Client(api_token=api_token)

    async def generate_image(self, label: str) -> str:
        try:
            return "https://picsum.photos/640/360"
            output = await asyncio.to_thread(
                self.client.run,
                self.model_id,
                input={
                    "prompt": label,
                    "aspect_ratio": "3:2"
                }
            )
        except ReadTimeout as e:
            raise RuntimeError(f"Replicate connection timed out: {e}") from e
        except ModelError as e:
            raise ValueError(f"Image model failed to generate result: {e}") from e
        except Exception as e:
            raise RuntimeError(f"Failed to generate image from prompt: {e}") from e

        if not output:
            raise ValueError("No image generated from prompt.")
        return str(output)

    async def generate_images(self, labels: list[str]) -> list[str]:
        tasks = [self.generate_image(label) for label in labels]
        return await asyncio.gather(*tasks)