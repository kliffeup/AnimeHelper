from anime_helper.anime_helper import AnimeHelper
from fire import Fire


def run():
    anime_helper = AnimeHelper()

    Fire({
        'find-season': anime_helper.get_seasonal_anime,
        'find-keyword': anime_helper.get_anime_by_keyword,
        'find-rank': anime_helper.get_anime_ranking,
        'info': anime_helper.get_anime_info,
    })
