from anime_helper.anime_helper import AnimeHelper, MangaHelper
from fire import Fire


def run():
    anime_helper = AnimeHelper()
    manga_helper = MangaHelper()

    Fire({
        'anime-season': anime_helper.get_seasonal_anime,
        'anime-info': anime_helper.get_info_by_id,
        'anime-keyword': anime_helper.find_by_keyword,
        'anime-rank': anime_helper.get_by_ranking,
        'manga-info': manga_helper.get_info_by_id,
        'manga-keyword': manga_helper.find_by_keyword,
        'manga-rank': manga_helper.get_by_ranking,
    })
