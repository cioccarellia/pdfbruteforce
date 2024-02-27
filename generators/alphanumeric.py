import itertools

def gen_alphanumeric(alphabet, guess_length):
    iterable = [alphabet] * guess_length
    combinations = itertools.product(*iterable)

    return itertools.starmap(lambda *args: ''.join(args), combinations)