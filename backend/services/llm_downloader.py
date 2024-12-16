from pathlib import Path

from utils.downloader import AsyncFileDownloader


class ModelDownloadService:
    def __init__(self, downloader: AsyncFileDownloader):
        """
        Initialize the ModelDownloadService with an AsyncFileDownloader dependency.

        :param downloader: An instance of AsyncFileDownloader for handling downloads
        """
        self.downloader = downloader
        self.progress = 0

    async def download_model(self, model_gguf_url: str, destination_path: Path) -> None:
        """
        Download a model if it doesn't already exist in the specified path or if the size does not match the expected.

        :param model_gguf_url: The URL of the model's gguf file
        :param destination_path: The path where the file should be saved
        :return: None
        """
        print(f"Downloading model {model_gguf_url} to {destination_path}")
        expected_size = await self.downloader.get_content_length()
        print(f"Expected size: {expected_size}")

        # Check if file exists and compare sizes
        if destination_path.exists():
            existing_size = destination_path.stat().st_size
            print(f"Existing size: {existing_size}")
            if existing_size == expected_size:
                print(f"File already exists at {destination_path} with expected size {expected_size}")
                self.progress = 100
                return
            else:
                print(f"File size mismatch, re-downloading...")
        else:
            print(f"File does not exist, creating new download...")

        try:
            # Ensure the directory exists
            destination_path.parent.mkdir(parents=True, exist_ok=True)

            # Open the file in write-binary mode
            with open(destination_path, 'wb') as file:
                async for chunk in self.downloader.download_chunks():
                    file.write(chunk)
                    self.progress = self.downloader.progress
                    print(f"Downloaded", self.progress, "%")

            actual_size = destination_path.stat().st_size
            if actual_size == expected_size:
                print(f"Model {model_gguf_url} downloaded successfully to {destination_path}")
            else:
                print(f"Warning: Downloaded file size {actual_size} does not match expected size {expected_size}")
        except Exception as e:
            print(f"Failed to download model {model_gguf_url}: {e}")
            raise

    def get_progress(self):
        return self.progress