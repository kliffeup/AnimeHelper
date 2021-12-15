from datetime import datetime as dt
import requests
from fire.core import _DictAsString


class AnimeHelper():
    def __init__(self):
        self._base_url = 'https://api.myanimelist.net/v2/anime'
        self._headers = {'X-MAL-Client-ID': '57121927cbbd32b51805997e72fc2496'}
        self._find_fields = (
            'id',
            'title',
            'genres',
            'synopsis',
        )

        self._info_fields = (
            'title',
            'alternative_titles',
            'start_date',
            'end_date',
            'synopsis',
            'mean',
            'rank',
            'popularity',
            'num_list_users',
            'num_scoring_users',
            'nsfw',
            'media_type',
            'status',
            'genres',
            'num_episodes',
            'source',
            'rating',
            'studios',
        )


    def _parse_json(self, response_json):
        if response_json and 'data' in response_json:
            list_response = []
            for json_obj in response_json['data']:
                cur_anime = {}
                if 'node' in json_obj:
                    for i in json_obj['node']:
                        cur_anime[i] = json_obj['node'][i]

                list_response.append(cur_anime)
            return list_response
        else:
            return response_json


    def _format_output(self, json_obj):
        if isinstance(json_obj, dict):
            del json_obj['main_picture']
            if 'genres' in json_obj:
                genres = []
                for genre in json_obj['genres']:
                    genres.append(genre['name'])

                json_obj['genres'] = ', '.join(genres)

            if 'alternative_titles' in json_obj:
                synonyms = json_obj['alternative_titles']['synonyms']
                en_title = json_obj['alternative_titles']['en']
                ja_title = json_obj['alternative_titles']['ja']

                alternative_titles = ', '.join(
                    filter(None, (*synonyms, en_title, ja_title))
                )

                json_obj['alternative_titles'] = alternative_titles

            if 'studios' in json_obj:
                studios = []
                for studio in json_obj['studios']:
                    studios.append(studio['name'])

                json_obj['studios'] = ', '.join(studios)

            return json_obj

        if isinstance(json_obj, list):
            for cur_anime in json_obj:
                print(_DictAsString(self._format_output(cur_anime)))
                print()


    def _execute_request(self, uri, params):
        url = self._base_url + uri
        response = requests.get(
            url=url,
            headers=self._headers,
            params=params,
        )

        if response.status_code < 400:
            return response.json()
        else:
            raise requests.RequestException(f'Request for {url} failed')


    def get_anime_info(self, anime_id):
        uri = f'/{anime_id}'
        params = {
            'fields': ','.join(self._info_fields),
        }

        response_json = self._execute_request(uri=uri, params=params)
        parsed_json = self._parse_json(response_json)
        return self._format_output(parsed_json)


    def get_anime_by_keyword(self, keyword, limit=10):
        uri = ''
        params = {
            'q': keyword,
            'fields': ','.join(self._find_fields),
            'limit': limit,
        }

        response_json = self._execute_request(uri=uri, params=params)
        parsed_json = self._parse_json(response_json)
        return self._format_output(parsed_json)


    def get_anime_ranking(self, ranking_type='all', limit=10):
        uri = '/ranking'
        ranking_types = (
            'all',
            'airing',
            'upcoming',
            'tv',
            'ova',
            'movie',
            'special',
            'bypopularity',
            'favorite',
        )

        if ranking_type not in ranking_types:
            print('Wrong ranking type occurred')
            print('Input correct ranking type:', ', '.join(ranking_types))
            return

        params = {
            'ranking_type': ranking_type,
            'fields': ','.join(self._find_fields),
            'limit': limit,
        }

        response_json = self._execute_request(uri=uri, params=params)
        parsed_json = self._parse_json(response_json)
        return self._format_output(parsed_json)


    def get_seasonal_anime(
        self, year=None, season=None, sort='anime_score', limit=10,
    ):
        if year is None:
            year = int(dt.now().year)

        if season is None:
            month_to_season = (
                'winter',
                'winter',
                'winter',
                'spring',
                'spring',
                'spring',
                'summer',
                'summer',
                'summer',
                'fall',
                'fall',
                'fall',
            )

            season = month_to_season[int(dt.now().month) - 1]

        seasons = ('winter', 'spring', 'summer', 'fall')
        if season not in season:
            print('Wrong season occurred')
            print('Input correct season:', ', '.join(seasons))
            return

        sort_options = ('anime_score', 'anime_num_list_users')
        if sort not in sort_options:
            print('Wrong sort option occurred')
            print('Input correct sort option:', ', '.join(sort_options))
            return

        uri = f'/season/{year}/{season}'
        params = {
            'sort': sort,
            'limit': limit,
            'fields': ','.join(self._find_fields),
        }

        response_json = self._execute_request(uri=uri, params=params)
        parsed_json = self._parse_json(response_json)
        return self._format_output(parsed_json)
