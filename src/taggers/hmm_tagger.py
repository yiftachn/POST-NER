from typing import List

from src.taggers.base_tagger import BaseTrigramTagger

class HMMTagger(BaseTrigramTagger):
    def _predict(self,sentence:str) ->List[str]:
        return ['NNP'] * len(sentence)
