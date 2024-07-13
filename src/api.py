from abc import ABC, abstractmethod

import requests
from tqdm import tqdm

from src.entities import Vacancy


class BaseVacanciesAPI(ABC):

    @abstractmethod
    def get_vacancies(self, search_text: str) -> list[dict]:
        pass


class HHVacanciesAPI(BaseVacanciesAPI):

    def get_vacancies(self, search_text: str) -> list[Vacancy]:
        url = 'https://api.hh.ru/vacancies'
        params = {
            'text': search_text,
            'only_with_salary': True,
            'per_page': 100,
        }

        raw_vacancies = self._get_list(url, params, max_pages=2)
        return [
            Vacancy(
                name=data['name'],
                url=data['alternate_url'],
                salary_currency=data['salary']['currency'],
                salary_from=data['salary']['from'],
                salary_to=data['salary']['to'],
            )
            for data in raw_vacancies
        ]

    def _get_list(self, url: str, params: dict, max_pages: int = 1) -> list[dict]:
        items = []
        for current_page in tqdm(range(0, max_pages)):
            params['page'] = current_page

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data['found'] == 0:
                break

            items.extend(data['items'])

        return items
