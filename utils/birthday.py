# from https://en.wikipedia.org/wiki/Birthday_attack#Source_code_example

from math import log1p, sqrt
from settings import r


def birthday(probability_exponent, bits):
    """
    Used to estimate the probability cookie segments will clash. Then multiply this result with the likelihood that two
    of the same first party sites are visited at once by users using the same public IP address.
    This creates the likelihood of a misrecorded history entry.

    Not used in the site. Only used to run locally for estimation.
    """
    probability = 10. ** probability_exponent
    print(probability)
    outputs = 2. ** bits
    print(outputs)
    print(sqrt(2. * outputs * -log1p(-probability)))


birthday(-2, 10)
r.flushall()
