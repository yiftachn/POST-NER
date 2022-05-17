import string
from pathlib import Path
from typing import List

from src.utils import parse_input_file
from src.utils import write_prediction_to_file, START, _convert_prediction_to_string, WordPos, PosTrigrams


class BaseTrigramTagger:
    def __init__(self, input_file: Path, prediction_file: Path, e_file: Path, q_file: Path):
        self.input_sentences = parse_input_file(input_file)
        self.word_pos_dict = WordPos(e_file)
        self.pos_trigram_dict = PosTrigrams(q_file)
        self.prediction_file: Path = prediction_file

    def write_prediction(self):
        prediction: List[str] = list(map(self.predict, self.input_sentences))
        write_prediction_to_file(prediction, self.prediction_file, self.input_sentences)

    def predict(self, sentence: str) -> str:
        sentence = sentence.lower()
        prediction = self._predict(sentence)
        return _convert_prediction_to_string(prediction)

    def _predict(self, sentence: str) -> List[str]:
        raise NotImplementedError
