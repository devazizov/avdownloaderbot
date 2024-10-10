from aiogram.utils.keyboard import InlineKeyboardBuilder

def generate_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="Video", callback_data="video")
    builder.button(text="Audio", callback_data="audio")

    return builder.as_markup()
    