from anime_helper import AnimeHelper
from fire import Fire


def run():
    kek = AnimeHelper()

    Fire({
        'find-season': kek.get_seasonal_anime,
        'find-keyword': kek.get_anime_by_keyword,
        'find-rank': kek.get_anime_ranking,
        'info': kek.get_anime_info,
    })
