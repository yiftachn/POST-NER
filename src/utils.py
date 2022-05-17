import re
from functools import reduce
from pathlib import Path
import string
from typing import List, Tuple

START = '#!'
UNKNOWN = '*UNK*'


def calculate_accuracy(prediction_file:Path,labeled_file:Path) -> float:
    with open(prediction_file,'r') as prediction_file, open(labeled_file,'r') as labeled_file:
        prediction_file = prediction_file.read()
        labeled_file = labeled_file.read()

    prediction_list = extract_tags(prediction_file)
    labeled_list = extract_tags(labeled_file)
    assert len(labeled_list) == len(prediction_list)

    return len(list(filter(lambda pair: pair[0] == pair[1],zip(prediction_list,labeled_list)))) / len(prediction_list)




def extract_tags(tagged_string, keep_start_mark=False):
    start_clause = f'|{START}' if keep_start_mark else ''
    return re.findall(f'/[A-Z{string.punctuation}]+{start_clause}', tagged_string)

if __name__ == '__main__':
    print(calculate_accuracy('../results/greedy_results.txt','../data/ass1-tagger-dev'))


class WordPos:
    def __init__(self, e_file: Path):
        with open(e_file, 'r') as file:
            file_content = file.read()
        rows = file_content.split('\n')
        rows.remove('')
        self.word_pos_dict = {}
        for row in rows:
            splited_row = row.split(' ')
            if len(splited_row) > 2:
                word = reduce(lambda old, new: old + ' ' + new, splited_row[:-1])
            else:
                word = splited_row[0]
            pos, count = splited_row[-1].split('\t')

            old_pos_list = self.word_pos_dict.get(word)
            new_pos_list = old_pos_list if old_pos_list is not None else []
            new_pos_list.append((pos, count))
            self.word_pos_dict.update({word: new_pos_list})

    def __getitem__(self, word):
        #todo: add the catch mechanism of the signatures
        try:
            return list(zip(*self.word_pos_dict[word]))[0]
        except KeyError:
            return list(zip(*self.word_pos_dict[UNKNOWN]))[0]

    def get_count(self, word, pos) -> int:
        try:
            pos_list = self.word_pos_dict[word]
        except KeyError:
            pos_list = self.word_pos_dict[UNKNOWN]
        correct_pos = list(filter(lambda pos_count: pos == pos_count[0], pos_list))[0]
        return int(correct_pos[1])


class PosTrigrams:
    def __init__(self, q_file: Path):
        with open(q_file, 'r') as file:
            file_content = file.read()
        rows = file_content.split('\n')
        rows.remove('')
        self.pos_trigram_dict = {}

        trigrams_rows = filter(lambda row: len(row.split(' ')) == 3, rows)
        for trigram in trigrams_rows:
            pos_in_row, count = trigram.split('\t')
            pos_in_row = pos_in_row.split(' ')
            main_pos = pos_in_row[-1]
            old_trigram_list = self.pos_trigram_dict.get(main_pos)
            new_trigram_list = old_trigram_list if old_trigram_list is not None else []
            new_trigram_list.append((pos_in_row, count))
            self.pos_trigram_dict.update({main_pos: new_trigram_list})

    def __getitem__(self, pos):
        return list(zip(*self.pos_trigram_dict[pos]))[0]

    def get_count(self, pos_list) -> int:
        trigram_list = self.pos_trigram_dict[pos_list[-1]]
        correct_trigram = list(filter(lambda pos_list_count_tuple: pos_list == pos_list_count_tuple[0], trigram_list))
        if len(correct_trigram) == 0:
            return 0
        else:
            return int(correct_trigram[0][1])


def parse_input_file(file_name: Path) -> List[str]:
    with open(file_name, 'r') as file:
        file_content = file.read()
    return file_content.split('\n')[:-1] # drop last ''


def write_prediction_to_file(predictions:List[str], prediction_file:Path, input_sentences:List[str]) -> str:
    file_content = ''
    tagged_sentences = map(add_tags_to_sentence, zip(input_sentences, predictions))
    for sentence in tagged_sentences:
        file_content += sentence +'\n'
    with open(prediction_file,'w') as file:
        file.write(file_content[:-1]) #skip last newline


def add_tags_to_sentence(sentence_prediction:Tuple[str,List[str]]) -> str:
    tagged_sentence = ''
    sentence,prediction = sentence_prediction
    for pair in zip(sentence.split(' '),prediction.split(' ')):
        tagged_sentence += pair[0]+'/'+pair[1] +' '
    tagged_sentence = tagged_sentence[:-1] #remove last space
    return tagged_sentence


def _convert_prediction_to_string(predicted_pos:List[str])->str:
    prediction_string = ''
    for pos in predicted_pos:
        prediction_string += pos + ' '
    return prediction_string[:-1] #without last space
