from pathlib import Path
from typing import AsyncGenerator

import aiohttp


class AsyncFileDownloader:
    def __init__(self, url: str, download_path: Path):
        """
        Initialize the downloader with URL and download path.

        Args:
            url: The URL of the file to download
            download_path: The directory where the file should be saved
        """
        self.url = url
        self.download_path = download_path
        self._total_size: int = 0
        self._downloaded_size: int = 0
        self._is_downloading: bool = False

    @property
    def progress(self) -> float:
        """
        Get the current download progress as a percentage.

        Returns:
            float: Progress percentage between 0 and 100
        """
        if not self._total_size:
            return 0

        return (self._downloaded_size / self._total_size) * 100

    async def download_chunks(self) -> AsyncGenerator[bytes, None]:
        """
        Download the file in chunks asynchronously.

        Yields:
            bytes: Each chunk of the file data

        Raises:
            RuntimeError: If a download is already in progress.
        """
        if self._is_downloading:
            raise RuntimeError("Download already in progress")

        self._is_downloading = True
        self._downloaded_size = 0

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url, ssl=False, timeout=0) as response:
                    response.raise_for_status()

                    self._total_size = int(response.headers.get('content-length', 0))

                    async for chunk in response.content.iter_chunked(8192):
                        self._downloaded_size += len(chunk)
                        yield chunk
        except Exception as e:
            raise e
        finally:
            self._is_downloading = False

    async def get_content_length(self) -> int:
        """
        Make a GET request to fetch only the content length of the file without downloading it.

        Returns:
            int: The size of the content in bytes as reported by the server or 0 if not available.

        Raises:
            aiohttp.ClientResponseError: If there's an error in the HTTP response.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, headers={'Accept-Encoding': 'identity'}, ssl=False) as response:
                response.raise_for_status()
                # We explicitly set 'Accept-Encoding' to 'identity' to avoid automatic decompression
                # which could alter the content length perceived by the client
                content_length = response.headers.get('Content-Length')
                return int(content_length) if content_length else 0
