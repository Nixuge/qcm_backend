from dataclasses import dataclass
from typing import Self


@dataclass
class Answer:
    text: str
    correct: bool

    @staticmethod
    def from_list(list: dict) -> Self | None:
        if list == None:
            return None

        answer_array: list[Answer] = []
        for answer_dict in list:
            answer_array.append(Answer.from_dict(answer_dict))

    @staticmethod
    def from_dict(dict: dict) -> Self:
        return Answer(
            text = dict.get("answer"),
            correct = bool(dict.get("correct"))
        )


@dataclass
class Question:
    main_question: str | None
    subquestion_1: str | None
    subquestion_2: str | None

    main_answers: list[Answer] | None
    subanswer_1: list[Answer] | None
    subanswer_2: list[Answer] | None
    
    explanation: str

    media_image: str
    question_audio: str
    explanation_audio: str

    # Unused for now, just using the json.
    @staticmethod
    def from_dict(dict: dict) -> Self:
        questions_dict = dict.get("questions")
        answers_dict = dict.get("answers")

        if not questions_dict or not answers_dict:
            raise Exception("Missing dicts !" + dict)
        
        return Question(
            main_question = questions_dict.get("0"),
            subquestion_1 = questions_dict.get("1"),
            subquestion_2 = questions_dict.get("2"),
            main_answers = Answer.from_list(answers_dict.get("0")),
            subanswer_1 = Answer.from_list(answers_dict.get("1")),
            subanswer_2 = Answer.from_list(answers_dict.get("2")),
            explanation = dict.get("explanation"),
            media_image = dict.get("media"),
            question_audio = dict.get("question_audio"),
            explanation_audio = dict.get("explanation_audio")
        )

