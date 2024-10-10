import yt_dlp
from tiktok_downloader import snaptik
from instagrapi import Client
import os


class YoutubeDownloader:
    def downloader_yt(self, video_url):
        # Video va audio ma'lumotlarni olish uchun sozlamalar
        # ydl_opts = {
        #     'format': 'bestaudio/best',  # Download the best available audio-only format
        #     'outtmpl': '%(title)s.%(ext)s',  # Name the file based on the video title
        # }

        # with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        #     info_dict = ydl.extract_info(video_url, download=False)
        #     audio_url = info_dict.get('url')
        #     thumbnail_url = info_dict.get('thumbnail', 'No thumbnail available')
        #     title = info_dict.get('title', 'No title available')

        # Video linkni olish uchun sozlamalar
        ydl_opts_video = {
            "format": "best",
            "noplaylist": True,
            "quiet": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts_video) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            video_url = info_dict.get("url")

        # `media` ro'yxati video va audio linklarni o'z ichiga oladi
        # media = [video_url, audio_url, thumbnail_url, title]

        media = video_url

        return media


class InstagramDownloader:

    def downloader_insta(self, video_url):

        username = "the_radnie"
        password = "donikot"

        session_file = f"{username}_session.json"

        cl = Client()

        if os.path.exists(session_file):
            cl.load_settings(session_file)
            cl.login(username, password)
        else:
            cl.login(username, password)
            cl.dump_settings(session_file)

        media_id = cl.media_pk_from_url(video_url)

        media_info = cl.media_info(media_id)

        return media_info


class TiktokDownloader:
    def downloader_tt(self, url):
        url = url
        video = snaptik(url)

        video = video[0].json

        if video.endswith("=1"):
            video = video[:-2]

        return video
