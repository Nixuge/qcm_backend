from dataclasses import dataclass, field
import json
import math
import random
from uuid import uuid4

from data.base_data import BaseData
from data.questions_data import QuestionsData
from data.types.question import Question

@dataclass
class Run:
    uuid: str
    selected_themes: list[str]
    question_count: int
    # list[("theme", "hash"), ("theme2", "hash2"), ...]
    # Note: moving to a list[tuple[str, Question]] would be nice to avoid parsing the dict every time,
    # but a bit more annoying for serialization.
    # For now this works well enough with a low performance hit, so leaving it be.
    questions: list[tuple[str, str]]
    current_question: int
    
    free_browsing: bool
    revealed_questions: list[int] = field(default_factory=list)
    answers_submitted: dict[int, dict] = field(default_factory=dict)

    def save_to_disk(self):
        with open(f"runs/ended/{self.uuid}.json", "w") as file:
            json.dump({
                "uuid": self.uuid, # redundant but might as well
                "free_browsing": self.free_browsing,
                "selected_themes": self.selected_themes,
                "questions": self.questions,
                "answers_submitted": self.answers_submitted
            }, file, indent = 4)

    # todo: have that store (& calculate?) which questions are good and which are bad
    def add_submitted_answers(self, question_number: int, answers: dict):
        self.revealed_questions.append(question_number)
        self.answers_submitted[question_number] = answers

    # to test
    def is_finished(self) -> bool:
        return len(self.revealed_questions) == self.question_count

    def can_access(self, index: int) -> bool:
        if self.free_browsing or index == 0:
            return True

        for discovered in self.revealed_questions:
            if index == discovered or index == discovered:
                return True
        return False

    def get_question_theme(self, index: int):
        return self.questions[index][0]
    def get_question_hash(self, index: int):
        return self.questions[index][1]


class RunBuilder:
    selected_themes: list[str]
    selected_themes_count: int
    question_count: int
    free_browsing: bool
    _base_question_per_theme: int
    _remaining: int
    _selected_questions: list[tuple[str, str]]
    _remaining_themes: list[str]

    def __init__(self, selected_themes: list[str], question_count: int, free_browsing: bool) -> None:
        self.selected_themes = selected_themes
        self.selected_themes_count = len(selected_themes)
        self.question_count = question_count
        self.free_browsing = free_browsing
        self._base_question_per_theme = math.floor(self.question_count / self.selected_themes_count)
        self._remaining = self.question_count % self.selected_themes_count
        self._selected_questions = []
        self._remaining_themes = []

    def _try_add_full_theme(self, theme: str, current_questions: dict[str, Question], len_current_questions: int) -> bool:
        if len_current_questions > self._base_question_per_theme:
            return False

        self._remaining += len_current_questions
        for question in current_questions.keys():
            self._selected_questions.append((theme, question))
        
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

    def _add_partial_theme(self, theme: str, current_questions: dict[str, Question], len_current_questions: int):
        self._remaining_themes.append(theme)
        indexes = self._get_unique_random_indexes_list_range(len_current_questions - 1)
        current_hashes = [*current_questions.keys()] # convert to a list
        for index in indexes:
            self._selected_questions.append((theme, current_hashes[index]))

    # Prolly inneficient as f too
    def _handle_remaining(self):
        while (self._remaining > 0):
            theme = random.choice(self._remaining_themes)
            question = random.choice([*QuestionsData.questions_dict[theme].keys()])
            value = (theme, question)
            if value not in self._selected_questions:
                self._selected_questions.append((theme, question))
                self._remaining -= 1

    def _make_question_list(self) -> str | None:
        for theme in self.selected_themes:
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
        
        random.shuffle(self._selected_questions)

 
    def build(self) -> Run | str:
        # Count checks
        if self.question_count > BaseData.MAX_QUESTION_COUNT:
            return "Too many questions"
        if self.question_count <= 0:
            return "Question count <= 0"

        if self.selected_themes_count > self.question_count: # may be removed ?
            return "More themes than questions"
        
        # If duplicates
        if self.selected_themes_count != len(set(self.selected_themes)):
            return "Duplicated themes in request"

        result = self._make_question_list()
        if result: return result
        

        return Run(
            uuid = uuid4().hex,
            selected_themes = self.selected_themes,
            question_count = self.question_count,
            questions = self._selected_questions,
            current_question = 1,
            free_browsing = self.free_browsing
        )