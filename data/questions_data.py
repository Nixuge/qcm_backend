# Meh file

class QuestionsData:
    themes = {}
    hashes: dict[str, list[str]] = {}
    questions_dict: dict[str, dict[str, dict]] = {} # to be loaded on startup
    answers_dict: dict[str, dict[str, dict]] = {}