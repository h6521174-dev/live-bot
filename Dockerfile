FROM python:3.10-slim
RUN apt-get update && apt-get install -y ffmpeg
WORKDIR /app
COPY . /app
RUN pip install pyrogram pytgcalls[video] nest_asyncio ffmpeg-python yt-dlp aiohttp TgCrypto
CMD ["python", "main.py"]
