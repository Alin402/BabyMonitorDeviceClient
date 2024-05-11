import subprocess
import asyncio


async def start_live_stream(event):
    try:
        print("Starting Livestream...")
        process = await asyncio.create_subprocess_shell(
            "libcamera-vid -t 0 --width 640 --height 362  --inline -o - | ffmpeg -re -ar 44100 -ac 2 -acodec pcm_s16le -f s16le -ac 2 -i /dev/zero -f h264 -i - -vcodec copy -acodec aac -ab 128k -g 50 -strict experimental -f flv rtmps://0679413b8dc3.global-contribute.live-video.net:443/app/sk_us-east-1_ypepuPhlQFgH_CCXiKGG9e1pDaaw0eL2Rq3SMxvjK7P",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        await process.communicate()

    except Exception as e:
        print("Exception:", e, type(e).__name__)