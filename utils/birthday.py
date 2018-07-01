# from https://en.wikipedia.org/wiki/Birthday_attack#Source_code_example

from math import log1p, sqrt
from settings import r


def birthday(probability_exponent, bits):
    probability = 10. ** probability_exponent
    print(probability)
    outputs = 2. ** bits
    print(outputs)
    print(sqrt(2. * outputs * -log1p(-probability)))


birthday(-2, 10)
r.flushall()
