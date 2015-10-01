from functions import *


def main():
    input_file_name, training_set_size, number_of_trials, verbose = get_args()
    data = parse_txt(input_file_name)
    train, test = data_split(data, training_set_size)
    names = train[0].keys()
    attributes = names[:len(names)-1]
    response = names[len(names)-1]
    id3(data, response, attributes)