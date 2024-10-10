import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters.command import CommandStart
from aiogram.types import (
    Message,
    InputMediaVideo,
    InputMediaPhoto,
    InputMediaAudio,
    InputMediaDocument,
)
from dotenv import load_dotenv

load_dotenv()

from downloader import YoutubeDownloader, InstagramDownloader, TiktokDownloader
from database import db

# from keyboards import generate_menu

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

dp = Dispatcher()
bot = Bot(token=BOT_TOKEN)

db.create_table()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        text=f"Hi <b>{message.from_user.full_name}</b>, this bot you can upload videos from youtube, instagram, tiktok quickly and easily, just send the video link :)\n\nIf you find any problem with the bot please let us know about it @azvdev\n\n<b>Follow the news @avdevblog</b>",
        parse_mode="HTML",
    )

    # Register Users

    users = db.all_users()

    bot_info = await bot.get_me()

    found = False

    for user in users:
        if str(message.from_user.id) in user["user_id"]:
            found = True

    if not found:

        db.register_user(
            message.from_user.full_name,
            message.from_user.id,
            message.from_user.username,
        )

        channel_message = f"<b>Which Bot:</b> {bot_info.first_name}\n<b>Bot username:</b> @{bot_info.username}\n\n<b>User:</b> {message.from_user.full_name}\n<b>Username:</b> @{message.from_user.username}\n<b>User ID:</b> {message.from_user.id}"
        await bot.send_message(
            chat_id=CHANNEL_ID, text=channel_message, parse_mode="HTML"
        )


@dp.message(lambda message: "tiktok.com" in message.text)
async def process_tiktok_url(message: Message):

    await bot.send_chat_action(message.chat.id, "upload_video")

    tiktok_url = message.text

    tiktok_dl = TiktokDownloader()

    video_url = tiktok_dl.downloader_tt(url=tiktok_url)

    await bot.send_video(chat_id=message.chat.id, video=video_url)

    # Register Users

    users = db.all_users()

    bot_info = await bot.get_me()

    found = False

    for user in users:
        if str(message.from_user.id) in user["user_id"]:
            found = True

    if not found:

        db.register_user(
            message.from_user.full_name,
            message.from_user.id,
            message.from_user.username,
        )

        channel_message = f"<b>Which Bot:</b> {bot_info.first_name}\n<b>Bot username:</b> @{bot_info.username}\n\n<b>User:</b> {message.from_user.full_name}\n<b>Username:</b> @{message.from_user.username}\n<b>User ID:</b> {message.from_user.id}"
        await bot.send_message(
            chat_id=CHANNEL_ID, text=channel_message, parse_mode="HTML"
        )


@dp.message(lambda message: "youtube.com" in message.text or "youtu.be" in message.text)
async def process_youtube_url(message: Message):
    global media_url

    youtube_url = message.text

    await bot.send_chat_action(message.chat.id, "upload_video")

    youtube_dl = YoutubeDownloader()

    media_url = youtube_dl.downloader_yt(youtube_url)

    await bot.send_video(chat_id=message.chat.id, video=media_url)

    # Register Users

    users = db.all_users()

    bot_info = await bot.get_me()

    found = False

    for user in users:
        if str(message.from_user.id) in user["user_id"]:
            found = True

    if not found:

        db.register_user(
            message.from_user.full_name,
            message.from_user.id,
            message.from_user.username,
        )

        channel_message = f"<b>Which Bot:</b> {bot_info.first_name}\n<b>Bot username:</b> @{bot_info.username}\n\n<b>User:</b> {message.from_user.full_name}\n<b>Username:</b> @{message.from_user.username}\n<b>User ID:</b> {message.from_user.id}"
        await bot.send_message(
            chat_id=CHANNEL_ID, text=channel_message, parse_mode="HTML"
        )


#     try:
#         print(media_url[1])
#         await bot.send_audio(chat_id=message.chat.id, audio=media_url[1])
#     except Exception as e:
#         print(e)


#     await bot.send_photo(chat_id=message.chat.id, photo=media_url[2], caption=media_url[3], reply_markup=generate_menu())


# @dp.callback_query(lambda c: c.data in ['video', 'audio'])
# async def handle_callback(callback_query: CallbackQuery):
#     chat_id = callback_query.from_user.id
#     data = callback_query.data

#     if data == 'video':
#         await bot.send_video(chat_id=chat_id, video=media_url[0], caption='Bu video.')
#     if data == 'audio':
#         print(media_url[1])
#         await bot.send_audio(chat_id=chat_id, audio=f"{media_url[1]}", caption='Bu audio.')


#     await bot.answer_callback_query(callback_query.id)


@dp.message(lambda message: "instagram.com" in message.text)
async def process_instagram_url(message: Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    video_url = message.text

    instagram_dl = InstagramDownloader()
    media_info = instagram_dl.downloader_insta(video_url)

    if media_info.product_type == "feed":
        await bot.send_chat_action(chat_id=message.chat.id, action="upload_photo")
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=media_info.image_versions2["candidates"][0]["url"],
        )

    if media_info.product_type == "carousel_container":
        media = []

        for resource in media_info.resources:
            if resource.media_type == 2:
                await bot.send_chat_action(
                    chat_id=message.chat.id, action="upload_video"
                )
                video_url = resource.video_url
                await bot.send_video(chat_id=message.chat.id, video=str(video_url))
            elif resource.media_type == 1:
                await bot.send_chat_action(
                    chat_id=message.chat.id, action="upload_photo"
                )
                photo_url = resource.thumbnail_url
                media.append(InputMediaPhoto(media=str(photo_url)))

        await bot.send_media_group(chat_id=message.chat.id, media=media)

    if media_info.product_type == "clips":
        await bot.send_chat_action(chat_id=message.chat.id, action="upload_video")

        await bot.send_video(chat_id=message.chat.id, video=str(media_info.video_url))

    users = db.all_users()

    bot_info = await bot.get_me()

    found = False

    for user in users:
        if str(message.from_user.id) in user["user_id"]:
            found = True

    if not found:

        db.register_user(
            message.from_user.full_name,
            message.from_user.id,
            message.from_user.username,
        )

        channel_message = f"<b>Which Bot:</b> {bot_info.first_name}\n<b>Bot username:</b> @{bot_info.username}\n\n<b>User:</b> {message.from_user.full_name}\n<b>Username:</b> @{message.from_user.username}\n<b>User ID:</b> {message.from_user.id}"
        await bot.send_message(
            chat_id=CHANNEL_ID, text=channel_message, parse_mode="HTML"
        )


@dp.message()
async def invalid_url(message: Message):
    await message.reply(
        text="Invlid url please send instagram youtube or tiktok link :)"
    )


async def main():

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
