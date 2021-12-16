from datetime import datetime as dt
import requests
from fire.core import _DictAsString


# 'https://api.myanimelist.net/v2/' 'https://myanimelist.net/'

class ApiCaller():
    def __init__(self, api_url, base_url, info_fields, ranking_types):
        self._api_url = api_url
        self._base_url = base_url
        self._headers = {'X-MAL-Client-ID': '57121927cbbd32b51805997e72fc2496'}
        self._find_fields = (
            'id',
            'title',
            'genres',
            'synopsis',
        )

        self._info_fields = info_fields
        self._ranking_types = ranking_types


    def _parse_json(self, response_json):
        if response_json and 'data' in response_json:
            list_response = []
            for json_obj in response_json['data']:
                cur_obj = json_obj.get('node', {})
                list_response.append(cur_obj)
            return list_response
        else:
            return response_json


    def _format_output(self, json_obj):
        if isinstance(json_obj, dict):
            del json_obj['main_picture']
            genres = (genre['name'] for genre in json_obj.get('genres', []))
            json_obj['genres'] = ', '.join(genres)

            if 'alternative_titles' in json_obj:
                synonyms, en_title, ja_title = map(
                    json_obj['alternative_titles'].get, ('synonyms', 'en', 'ja')
                )

                alternative_titles = ', '.join(
                    filter(None, (*synonyms, en_title, ja_title))
                )

                json_obj['alternative_titles'] = alternative_titles

            return json_obj

        if isinstance(json_obj, list):
            for cur_obj in json_obj:
                print(_DictAsString(self._format_output(cur_obj)))
                print()


    def _execute_request(self, uri, params):
        url = self._api_url + uri
        response = requests.get(
            url=url,
            headers=self._headers,
            params=params,
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise requests.RequestException(f'Request for {url} failed')


    def get_info_by_id(self, id):
        uri = f'/{id}'
        params = {
            'fields': ','.join(self._info_fields),
        }

        response_json = self._execute_request(uri=uri, params=params)
        parsed_json = self._parse_json(response_json)
        if isinstance(parsed_json, dict):
            parsed_json['url'] = self._base_url + uri

        return self._format_output(parsed_json)


    def find_by_keyword(self, keyword, limit=10):
        uri = ''
        params = {
            'q': str(keyword),
            'fields': ','.join(self._find_fields),
            'limit': limit,
        }

        response_json = self._execute_request(uri=uri, params=params)
        parsed_json = self._parse_json(response_json)
        return self._format_output(parsed_json)


    def get_by_ranking(self, ranking_type='all', limit=10):
        uri = '/ranking'
        if ranking_type not in self._ranking_types:
            print('Wrong ranking type occurred')
            print('Input correct ranking type:', ', '.join(self._ranking_types))
            return

        params = {
            'ranking_type': ranking_type,
            'fields': ','.join(self._find_fields),
            'limit': limit,
        }

        response_json = self._execute_request(uri=uri, params=params)
        parsed_json = self._parse_json(response_json)
        return self._format_output(parsed_json)


class AnimeHelper(ApiCaller):
    def __init__(self):
        super().__init__(
            api_url='https://api.myanimelist.net/v2/anime',
            base_url='https://myanimelist.net/anime',
            info_fields=(
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
            ),
            ranking_types=(
                'all',
                'airing',
                'upcoming',
                'tv',
                'ova',
                'movie',
                'special',
                'bypopularity',
                'favorite',
            ),
        )


    def _format_output(self, json_obj):
        if isinstance(json_obj, dict):
            studios = (studio['name'] for studio in json_obj.get('studios', []))
            json_obj['studios'] = ', '.join(studios)

        return super()._format_output(json_obj)


    def get_seasonal_anime(
        self, year=None, season=None, sort='anime_score', limit=10,
    ):
        year = year or int(dt.now().year)
        seasons = ('winter', 'spring', 'summer', 'fall')

        if season is None:
            month_to_season = [season for season in seasons for _ in range(3)]
            season = month_to_season[int(dt.now().month) - 1]

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


class MangaHelper(ApiCaller):
    def __init__(self):
        super().__init__(
            api_url='https://api.myanimelist.net/v2/manga',
            base_url='https://myanimelist.net/manga',
            info_fields=(
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
                'num_volumes',
                'num_chapters',
                'authors',
                'genres',
            ),
            ranking_types=(
                'all',
                'manga',
                'novels',
                'oneshots',
                'doujin',
                'manhwa',
                'manhua',
                'bypopularity',
                'favorite',
            ),
        )


    def _format_output(self, json_obj):
        if 'authors' in json_obj:
            authors = (
                str(a['node']['id']) for a in json_obj.get('authors', [])
            )

            json_obj['authors'] = ', '.join(authors)

        return super()._format_output(json_obj)
