import itertools

def gen_dictionary(dictionary, length):
    iterable = [dictionary] * length
    combinations = itertools.product(*iterable)
    return itertools.starmap(lambda *args: ''.join(args), combinations)