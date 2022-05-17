from typing import List

from src.taggers.base_tagger import BaseTrigramTagger
from src.utils import START


class GreedyTagger(BaseTrigramTagger):
    def _predict(self,sentence:str) ->List[str]:
        prediction = [START,START]
        for index, word in enumerate(sentence.split(' ')):
            max_p_pos = 0
            possible_pos = self.word_pos_dict[word]
            for suggested_pos in possible_pos:
                trigram = prediction[index:index + 2] + [suggested_pos]
                p_pos = self.pos_trigram_dict.get_count(trigram) * self.word_pos_dict.get_count(word, suggested_pos)
                if p_pos >= max_p_pos:
                    max_p_pos = p_pos
                    best_pos: str = suggested_pos
            prediction.append(best_pos)
        return prediction[2:]
