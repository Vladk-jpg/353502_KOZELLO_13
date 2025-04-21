import math
from utils.inputs import random_sequence


class SequenceCalculator:
    """
    A class for calculating the natural logarithm of (1 + x) using Taylor
    series expansion.
    """
    def calculate_ln(self, x, eps):
        """
        Calculates the natural logarithm of (1 + x) using the Taylor series
        approximation.

        Args:
            x (float): The value of x for the approximation.
            eps (float): The precision threshold for the approximation.

        Returns:
            tuple: A tuple containing the values:
                - x (float): The input value.
                - n (int): The number of terms used in the approximation.
                - fx (float): The approximated value of ln(1 + x).
                - m_fx (float): The true value of ln(1 + x).
                - eps (float): The epsilon value.
        """
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
        """
        Generates a sequence of logarithmic approximations for values from
        start to finish, incrementing by d.

        Args:
            start (float): The starting value of x.
            finish (float): The ending value of x.
            d (float): The step size for generating x values.
            eps (float): The precision threshold for the approximation.

        Returns:
            list: A list of tuples containing the results of `calculate_ln`
            for each x value.
        """
        arr = []
        x = start
        while x <= finish:
            arr.append(self.calculate_ln(x, eps))
            x += d
        return arr

    def generate_random_seq(self, count, eps):
        """
        Generates a sequence of random x values and calculates the logarithmic
        approximation for each using the `calculate_ln` method.

        Args:
            count (int): The number of random x values to generate.
            eps (float): The precision threshold for the approximation.

        Returns:
            list: A list of tuples containing the results of `calculate_ln`
            for each random x value.
        """
        arr = random_sequence(float, 0, 1, count)
        res = []
        for x in arr:
            res.append(self.calculate_ln(x, eps))
        return res
