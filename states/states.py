from aiogram.dispatcher.filters.state import StatesGroup, State

class download_by_name(StatesGroup):
    song_name = State()

class download_from_playlist(StatesGroup):
    beta = State()
    playlist_link = State()