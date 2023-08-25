from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Answer:
    text: str
    correct: bool

    def tuple(self) -> tuple[str, bool]:
        return (self.text, self.correct)

    @staticmethod
    def from_list(dict_list: dict) -> list[Answer]:
        if dict_list == None:
            return [] # Not the best optimization wise, but easier code wise

        answer_array: list[Answer] = []
        for answer_dict in dict_list:
            answer_array.append(Answer.from_dict(answer_dict))
        
        return answer_array

    @staticmethod
    def from_dict(dict: dict) -> Answer:
        return Answer(
            text = dict.get("answer", None),
            correct = bool(dict.get("correct"))
        )

# TODO:
# Have a more modular system
# where you can have as many subquestions/questions as you want

@dataclass
class Question:
    main_question: str | None
    subquestion_1: str | None
    subquestion_2: str | None

    main_answers: list[Answer]
    subanswers_1: list[Answer]
    subanswers_2: list[Answer]
    
    explanation: str

    media_image: str
    question_audio: str
    explanation_audio: str

    # To be used on initial question load
    def get_dict_no_full_answer(self):
        return {
            "main_question": self.main_question,
            "subquestion_1": self.subquestion_1,
            "subquestion_2": self.subquestion_2,
            "main_answers:": [answer.text for answer in self.main_answers],
            "subanswers_1:": [answer.text for answer in self.subanswers_1],
            "subanswers_2:": [answer.text for answer in self.subanswers_2],
            "media_image": self.media_image,
            "question_audio": self.question_audio
        }

    # To be used when getting reloading in the middle of a run
    # (eg on question 5, already answered the 4 previous ones,
    # in that case load the data from the previous ones from there)
    def get_dict_full(self):
        return {
            "main_question": self.main_question,
            "subquestion_1": self.subquestion_1,
            "subquestion_2": self.subquestion_2,
            "main_answers:": [answer.tuple() for answer in self.main_answers],
            "subanswers_1:": [answer.tuple() for answer in self.subanswers_1],
            "subanswers_2:": [answer.tuple() for answer in self.subanswers_2],
            "media_image": self.media_image,
            "question_audio": self.question_audio,
            "explanation": self.explanation,
            "explanation_audio": self.explanation_audio
        }
    
    # To be used when validating questions
    def get_answer_only_dict(self):
        return {
            "main_answers:": [answer.correct for answer in self.main_answers],
            "subanswers_1:": [answer.correct for answer in self.subanswers_1],
            "subanswers_2:": [answer.correct for answer in self.subanswers_2],
        }

    @staticmethod
    def from_dict(dict: dict) -> Question:
        questions_dict = dict.get("questions")
        answers_dict = dict.get("answers")

        if not questions_dict or not answers_dict:
            raise Exception(f"Missing dicts ! {dict}")
        
        return Question(
            main_question = questions_dict.get("0"),
            subquestion_1 = questions_dict.get("1"),
            subquestion_2 = questions_dict.get("2"),
            main_answers = Answer.from_list(answers_dict.get("0")),
            subanswers_1 = Answer.from_list(answers_dict.get("1")),
            subanswers_2 = Answer.from_list(answers_dict.get("2")),
            explanation = dict.get("explanation", None),
            media_image = dict.get("media", None),
            question_audio = dict.get("question_audio", None),
            explanation_audio = dict.get("explanation_audio", None)
        )

