import math
from utils.inputs import random_sequence


class SequenceCalculator:
    def calculate_ln(self, x, eps):
        n = 0
        m_fx = math.log(1 + x)
        fx = 0.0
        for i in range(1, 501):
            fx += (-1) ** (i - 1) * (x ** i) / i
            n += 1
            if math.fabs(fx - m_fx) < eps:
                break
        return (x, n, fx, m_fx, eps)

    def generate_sequence(self, start, finish, d, eps):
        arr = []
        x = start
        while x <= finish:
            arr.append(self.calculate_ln(x, eps))
            x += d
        return arr

    def generate_random_seq(self, count, eps):
        arr = random_sequence(float, 0, 1, count)
        res = []
        for x in arr:
            res.append(self.calculate_ln(x, eps))
        return res
