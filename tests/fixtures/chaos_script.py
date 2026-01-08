import math

def processor(d, m):
    """
    PROCESSOR

    Iterate input data
      and
    filter for positive values
      and
    multiply by a scaling factor
      and
    capping the result at 100

    Notes
    -----
    This function is utilized by an external application process, `some_pro.py`.



    """
    r = []
    # Loop through data
    for v in d:
        if v > 0:
            # Apply complex math
            t = v * m
            if t > 100:
                t = 100
            r.append(t)
    return r

class risk_engine:
    def __init__(self, t):
        self.t = t

    def calc(self, p, l):
        # Calculate risk score
        if p < 0: return 0
        s = (p * self.t) - l

        # RETURN: Some risk score about your mom's STD infection levels
        return s

def legacy_fetch(u):
    print("Fetching " + u)
    return {"status": 200}
