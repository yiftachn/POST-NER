from collections import Counter
from pathlib import Path
from typing import List
import argparse
import re

parser = argparse.ArgumentParser(description='Get args from bash')
parser.add_argument('input_file_name', metavar='i', type=str, nargs=1)
parser.add_argument('q_output_file', metavar='q', type=str, nargs=1)
parser.add_argument('e_output_file', metavar='e', type=str, nargs=1)

base_path = Path('./')


def main():

    args = parser.parse_args()
    input_file = _read_file(args.input_file_name[0])
    q_output_file = base_path / Path(args.q_output_file[0])
    e_output_file = base_path / Path(args.e_output_file[0])


    write_q_mle(input_file,q_output_file)
    write_e_mle(input_file,e_output_file)


def _read_file(filename:Path)-> str:
    with open(filename,'r') as file:
        file_content  = file.read()
    return file_content

def parse_input_file(file_content:str) -> List[str]:
    string_without_newlines = file_content.replace('\n',' ')
    events = string_without_newlines.split(' ')
    events.remove('')
    return events

def write_q_mle(file_content: str,q_output_file:Path) -> None:
    tags_list = re.findall('/[A-Z]+',file_content)
    two_grams = zip(*[tags_list[i:] for i in range(2)])
    counter = Counter(two_grams)
    file_content = ''
    for event in counter.keys():
        for item in event:
            file_content += str(item) + ' '
        file_content += '\t' + str(counter[event]) + '\n'
    file_content = file_content.replace('/','')
    with open(q_output_file,'w') as file:
        file.write(file_content)

def write_e_mle(file_content: str,e_output_file:Path) -> None:
    events_list = parse_input_file(file_content)
    events_count_string = _generate_events_counts_string(events_list)
    words_signatures_events = _generate_word_signature_string()
    with open(e_output_file,'w') as file:
        file.write(events_count_string + words_signatures_events)


def _generate_events_counts_string(events_list: List[str]) -> str:
    counter = Counter(events_list)
    file_content = ''
    for event in counter.keys():
        file_content += event + '\t' + str(counter[event]) + '\n'
    file_content = file_content.replace('/', ' ')
    return file_content

def _generate_word_signature_string() -> str:
    return ''

if __name__ == '__main__':
    main()



    #