# Meh file

from data.types.question import Question


class QuestionsData:
    themes = {}
    hashes: dict[str, list[str]] = {}
    questions_dict: dict[str, dict[str, Question]] = {} # to be loaded on startup
    # Bit of a mess
    # Format:
    # {
    #   "theme1": {
    #       "hash1": Question1
    #       "hash2": Question2
    #   }, 
    #   "theme2": {
    #       "hash1": Question1
    #       "hash2": Question2
    #       ...
    #   },
    #   ...
    # }