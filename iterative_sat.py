from __future__ import division
from __future__ import print_function

from watchlist import setup_watchlist
from watchlist import update_watchlist


__author__ = 'Sahand Saba'
__email__ = 'sahands@gmail.com'


def solve(instance, verbose=False):
    watchlist = setup_watchlist(instance)
    if not watchlist:
        return

    # The state list wil keep track of what values for which variables
    # we have tried so far. A value of 0 means nothing has been tried yet,
    # a value of 1 means False has been tried but not True, 2 means True but
    # not False, and 3 means both have been tried.
    state = [0] * instance.n
    assignment = [None] * instance.n
    d = 0  # Current depth in the backtrack tree
    while True:
        if d == instance.n:
            yield assignment
            d -= 1
            continue
        # Let's try assigning a value to v. Here would be the place to insert
        # heuristics of which value to try first.
        tried_something = False
        for a in [0, 1]:
            if (state[d] >> a) & 1 == 0:
                tried_something = True
                # Set the bit indicating a has been tried for d
                state[d] |= 1 << a
                assignment[d] = a
                if not update_watchlist(instance, watchlist,
                                        d << 1 | 1 ^ a,
                                        assignment,
                                        verbose):
                    assignment[d] = None
                else:
                    d += 1
                    break

        if not tried_something:
            if d == 0:
                # Can't backtrack further. No solutions.
                return
            else:
                # Backtrack
                state[d] = 0
                assignment[d] = None
                d -= 1