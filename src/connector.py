import json
from abc import ABC, abstractmethod
from dataclasses import asdict
from pathlib import Path

from src.entities import Vacancy


class Connector(ABC):

    @abstractmethod
    def get_vacancies(self) -> list[Vacancy]:
        pass

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        pass

    @abstractmethod
    def remove_vacancy(self, vacancy: Vacancy) -> None:
        pass

    @staticmethod
    def _parse_vacancy_to_dict(vacancy: Vacancy) -> dict:
        return asdict(vacancy)

    @staticmethod
    def _parse_dict_to_vacancy(raw_data: dict) -> Vacancy:
        return Vacancy(**raw_data)


class JsonConnector(Connector):

    def __init__(self, file_path: Path, encoding: str = 'utf-8') -> None:
        self.file_path = file_path
        self.encoding = encoding

    def get_vacancies(self) -> list[Vacancy]:
        if not self.file_path.exists():
            return []

        vacancies = []
        with self.file_path.open(encoding=self.encoding) as f:
            for item in json.load(f):
                vacancy = self._parse_dict_to_vacancy(item)
                vacancies.append(vacancy)
        return vacancies

    def add_vacancy(self, vacancy: Vacancy) -> None:
        vacancies = self.get_vacancies()
        if vacancy not in vacancies:
            vacancies.append(vacancy)
            self._save(*vacancies)

    def remove_vacancy(self, vacancy: Vacancy) -> None:
        vacancies = self.get_vacancies()
        if vacancy in vacancies:
            vacancies.remove(vacancy)
            self._save(*vacancies)

    def _save(self, *vacancies: Vacancy) -> None:
        raw_data = [self._parse_vacancy_to_dict(vac) for vac in vacancies]
        with self.file_path.open(mode='w', encoding=self.encoding) as file:
            json.dump(raw_data, file, indent=2, ensure_ascii=False)
