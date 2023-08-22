from dataclasses import dataclass
import math
import random
from typing import Self
from uuid import uuid4

from data.base_data import BaseData
from data.questions_data import QuestionsData

@dataclass
class Run:
    uuid: str
    selected_themes: list[str]
    question_count: int
    questions: dict[str, list[str]]


class RunBuilder:
    selected_themes: list[str]
    selected_themes_count: int
    question_count: int
    _base_question_per_theme: int
    _remaining: int
    _selected_questions: dict[str, list[str]]
    _remaining_themes: list[str]

    def __init__(self, selected_themes: list[str], question_count: int) -> None:
        self.selected_themes = selected_themes
        self.selected_themes_count = len(selected_themes)
        self.question_count = question_count
        self._base_question_per_theme = math.floor(self.question_count / self.selected_themes_count)
        self._remaining = self.question_count % self.selected_themes_count
        self._selected_questions = {}
        self._remaining_themes = []

    def _try_add_full_theme(self, theme: str, current_questions: dict[str, dict], len_current_questions: int) -> bool:
        if len_current_questions > self._base_question_per_theme:
            return False

        remaining += len_current_questions
        for question in current_questions.keys():
            self._selected_questions[theme].append(question)
        
        return True

    # Partially found on geeksforgeeks, prolly inneficient tbh
    def _get_unique_random_indexes_list_range(self, max_index: int):
        arr = []
        tmp = random.randint(0, max_index)
        
        for _ in range(self._base_question_per_theme):
            while tmp in arr: # meh
                tmp = random.randint(0, max_index)
            arr.append(tmp)
        
        return arr

    def _add_partial_theme(self, theme: str, current_questions: dict[str, dict], len_current_questions: int):
        self._remaining_themes.append(theme)
        indexes = self._get_unique_random_indexes_list_range(len_current_questions - 1)
        current_hashes = [*current_questions.keys()] # convert to a list
        for index in indexes:
            self._selected_questions[theme].append(current_hashes[index])

    # Prolly inneficient as f too
    def _handle_remaining(self):
        while (self._remaining > 0):
            theme = random.choice(self._remaining_themes)
            question = random.choice([*QuestionsData.questions_dict[theme].keys()])
            if question not in self._selected_questions[theme]:
                self._selected_questions[theme].append(question)
                self._remaining -= 1

    def _make_question_list(self) -> dict[str, list[str]]:
        for theme in self.selected_themes:
            self._selected_questions[theme] = []
            current_questions = QuestionsData.questions_dict.get(theme)

            if not current_questions:
                return "Theme " + theme + " doesn't exist."
            
            l = len(current_questions)
            # Either add full theme if makes the full base length,
            # otherwise add it partially w randomly selected indexes
            # (ngl not even sure if the first function works rn)
            if not self._try_add_full_theme(theme, current_questions, l):
                self._add_partial_theme(theme, current_questions, l)
            
        self._handle_remaining()

 
    def build(self) -> Run | str:
        # Count checks
        if self.question_count > BaseData.MAX_QUESTION_COUNT:
            return "Too many questions"

        if self.selected_themes_count > self.question_count: # may be removed ?
            return "More themes than questions"
        
        # If duplicates
        if self.selected_themes_count != len(set(self.selected_themes)):
            return "Duplicated themes in request"

        self._make_question_list()

        return Run(
            uuid = uuid4().hex,
            selected_themes = self.selected_themes,
            question_count = self.question_count,
            questions = self._selected_questions
        )