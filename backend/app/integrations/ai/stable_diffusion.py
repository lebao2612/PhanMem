import asyncio
from httpx import ReadTimeout
from replicate import async_run
from replicate.exceptions import ModelError


class StableDiffusionClient:
    def __init__(self, model_id: str, api_token: str):
        self.model_id = model_id
        self.api_token = api_token

    async def generate_image(self, label: str) -> str:
        # Tạm thời dùng ảnh demo nếu chưa gọi thật
        return "https://picsum.photos/640/360"

        try:
            output = await async_run(
                self.model_id,
                input={"prompt": label, "num_outputs": 1},
                api_token=self.api_token
            )
        except ReadTimeout:
            raise RuntimeError("Replicate connection timed out.")
        except ModelError:
            raise ValueError("Image model failed to generate result.")
        except Exception as e:
            raise RuntimeError("Failed to generate image from prompt.") from e

        if not output:
            raise ValueError("No image generated from prompt.")
        try:
            return output[0].url
        except Exception:
            raise RuntimeError("No image URL in result.")

    async def generate_images(self, labels: list[str]) -> list[str]:
        tasks = [self.generate_image(label) for label in labels]
        return await asyncio.gather(*tasks)