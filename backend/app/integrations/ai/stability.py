import asyncio
import replicate
from httpx import ReadTimeout
from replicate.exceptions import ModelError

class StabilityClient:
    def __init__(self, model_id: str, api_token: str):
        self.model_id = model_id
        self.api_token = api_token
        self.client = replicate.Client(api_token=api_token)

    async def generate_image(self, label: str) -> str:
        # Tạm thời dùng ảnh demo nếu chưa gọi thật
        # return "https://picsum.photos/640/360"

        try:
            output = await asyncio.to_thread(
                self.client.run,
                self.model_id,
                input={
                    "prompt": label,
                    "negative_prompt": "blurry, deformed, lowres, bad anatomy",
                    "guidance": 7.0,
                    "steps": 20,
                    "width": 576,
                    "height": 1024,
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