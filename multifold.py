from collections import deque, namedtuple
from sys import exit


Element = namedtuple('Element', 'date values')


def get_dates(x):
    """ Retrieves dates, used in the backtest function.

    Keyword arguments:
        x -- a deque of maxlength 2, each element of which is a named tuple
        with a field 'date'
    """
    old, new = (0, 1)
    return(x[old].date, x[new].date)


def update_state(h, r):
    """ Propagates a portfolio to the next date.
    """
    return({k: h[k]*(r[k] + 1) for k in h.keys()})


def compute_nmv(x):
    """ Compute the net market value of a portfolio.
    """
    return(sum(x.values()))


def compute_gmv(x):
    """ Compute the gross market value of a portfolio.
    """
    return(sum([abs(v) for v in x.values()]))


def rescale_state(h_old, r, h_new):
    h_old = update_state(h_old, r)
    rescale_factor = compute_gmv(h_old) / compute_gmv(h_new)
    return({k: rescale_factor * v for k, v in h_new.items()})


def backtester(holdings, rets):
    """ Generates propagated portfolios from holding data and returns.

    The function can be abstracted further by replacing Element.values with
    an arbitrary portfolio object and by providing separate_state and
    rescale_state functions.

    Keyword arguments:
    holdings -- iterable object returning a tuple. First field of the tuple is
    a date and second is a dictionary where keys are ids and values are
    holdings.
    rets -- iterable object returning a tuple. First field of the tuple is
    a date and second is a dictionary where keys are ids and values are returns.

    Returns an iterable: a tuple composed of a date and holdings dictionary.
    """
    old, new = (0, 1)
    PORT = deque(maxlen=2)
    HOLD = deque(maxlen=2)
    RETS = deque(maxlen=2)
    HOLD.append(next(holdings))
    RETS.append(next(rets))
    date_h, _ = get_dates(HOLD)
    date_r, _ = get_dates(RETS)
    PORT.append(HOLD[old])
    yield(PORT[old])
    for h in holdings:
        HOLD.append(h)
        for r in rets:
            RETS.append(r)
            date_r, date_r_next = get_dates(RETS)
            dte_h, date_h_next = get_dates(HOLD)
            if date_r >= date_h and date_r_next < date_h_next:
                port_next = update_state(PORT[old].values,
                                         RETS[old].values)
                PORT.append(Element(date=date_r_next, values=port_next))
                yield(PORT[new])
            elif date_r == date_h_next:
                port_next = rescale_state(PORT[old].values,
                                          RETS[old].values,
                                          HOLD[new].values)
                PORT.append(Element(date=date_r_next, value=port_next))
                yield(PORT[new])
                break
            elif date_r > date_h_next:
                exit('return dates do not contain holding dates')


def compute_returns(holdings):
    """ Generates propagated portfolios from holding data and returns.
    """
    old, new = (0, 1)
    PORT = deque(maxlen=2)
    PORT.append(next(holdings))
    for h in holdings:
        PORT.append(next(holdings))
        pnl = compute_nmv(PORT[new].values) - compute_nmv(PORT[old].values)
        gmv = compute_gmv(PORT[old].values)
        yield({'date': PORT[new].date, 'pnl': pnl, 'gmv': gmv, 'ret': pnl/gmv})


def reader(fname, sep=','):
    with open(fname, 'r') as f:
        line = next(f)
        id_names = [x.strip() for x in line.split(sep)]
        num_names = len(id_names)
        for line in f:
            x = line.split(sep)
            d = x[0].strip()
            v = {id_names[i]: float(x[1+i]) for i in range(num_names)}
            yield Element(date=d, values=v)


if __name__ == '__main__':
    print(0)
