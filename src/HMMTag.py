import argparse
from pathlib import Path

from src.taggers.hmm_tagger import HMMTagger
from src.utils import calculate_accuracy

parser = argparse.ArgumentParser(description='Get args from bash')
parser.add_argument('input_file_name', metavar='i', type=str, nargs=1)
parser.add_argument('q_file', metavar='q', type=str, nargs=1)
parser.add_argument('e_file', metavar='e', type=str, nargs=1)
parser.add_argument('prediction_file', metavar='p', type=str, nargs=1)
parser.add_argument('--extra_file', metavar='x', type=str, nargs=1, required=False)


#todo: you need to add protection from unseen transition in q, using interpolation.

def main() -> None:
    args = parser.parse_args()
    input_file_path = Path(args.input_file_name[0])
    prediction_file_path = Path(args.prediction_file[0])

    tagger = HMMTagger(input_file=input_file_path,prediction_file=prediction_file_path,q_file=args.q_file[0],e_file=args.e_file[0])
    tagger.write_prediction()
    print(f'Greedy tag Accuracy is {calculate_accuracy(prediction_file_path,"../data/ass1-tagger-dev")}')


if __name__ == '__main__':
    main()
