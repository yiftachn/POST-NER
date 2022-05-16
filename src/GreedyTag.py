import argparse
from functools import reduce
from pathlib import Path
from typing import List

parser = argparse.ArgumentParser(description='Get args from bash')
parser.add_argument('input_file_name', metavar='i', type=str, nargs=1)
parser.add_argument('q_file', metavar='q', type=str, nargs=1)
parser.add_argument('e_file', metavar='e', type=str, nargs=1)
parser.add_argument('prediction_file', metavar='p', type=str, nargs=1)
parser.add_argument('--extra_file', metavar='x', type=str, nargs=1, required=False)

args = parser.parse_args()
input_file_name = args.input_file_name[0]
q_file = open(args.q_file[0], 'r').read()


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
        return list(zip(*self.word_pos_dict[word]))[0]

    def get_count(self, word, pos) -> int:
        pos_list = self.word_pos_dict[word]
        correct_pos = list(filter(lambda pos_count: pos == pos_count[0], pos_list))[0]
        return int(correct_pos[1])


class PosTrigrams:
    def __init__(self, q_file: Path):
        with open(q_file, 'r') as file:
            file_content = file.read()
        rows = file_content.split('\n')
        rows.remove('')
        # todo: add START mark to q.mle

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
        correct_trigram = list(filter(lambda pos_list_count_tuple: pos_list == pos_list_count_tuple[0], trigram_list))[0]
        return int(correct_trigram[1])


word_pos_dict = WordPos(args.e_file[0])
pos_trigram_dict = PosTrigrams(args.q_file[0])


def main() -> None:
    sentences: List[List[str]] = parse_input_file(input_file_name)
    greedy_prediction(sentences[0])
    prediction: List[str] = map(greedy_prediction, sentences)
    # write_file_content(prediction)


def parse_input_file(file_name: Path) -> List[List[str]]:
    with open(file_name, 'r') as file:
        file_content = file.read()
    return file_content.split('\n')


def greedy_prediction(sentence: List[str]) -> str:
    prediction_string = ''
    max_p_pos = 0
    for word in sentence.split(' '):
        word = word.lower()
        possible_pos = word_pos_dict[word]
        for pos_for_word in possible_pos:
            # todo: ',' seenms to be missing from q.mle
            possible_trigrams = pos_trigram_dict[pos_for_word]
            for trigram in possible_trigrams:
                p_pos = pos_trigram_dict.get_count(trigram) * word_pos_dict.get_count(word,pos_for_word)
                if p_pos >= max_p_pos:
                    max_p_pos = p_pos
                    best_pos:str = trigram[-1]
        prediction_string += best_pos +' '

    # todo: handle space in the end of line


def get_possible_pos_for_word(word: str) -> List[WordPos]:
    # todo: word in row is not good enough, think of the word I. you need to lower case btw
    possible_e_file_rows = list(
        filter(lambda row: word in reduce(lambda old, new: old + ' ' + new, row.split(' ')[:-1]), e_file.split('\n')))
    possible_row_pos = []
    for row in possible_e_file_rows:
        possible_row_pos.append(WordPos(row))
    return possible_row_pos


if __name__ == '__main__':
    main()
