from utils.inputs import valid_input
import numpy as np


class Matrix:
    """
    A class that represents a matrix with random integer values.

    Attributes:
        rows (int): The number of rows in the matrix.
        columns (int): The number of columns in the matrix.
        data (numpy.ndarray): The matrix data.
    """

    def __init__(self, rows, columns):
        """
        Initializes a matrix with the given number of rows and columns.

        Args:
            rows (int): The number of rows in the matrix.
            columns (int): The number of columns in the matrix.
        """
        self.rows = rows
        self.columns = columns
        self.data = np.empty((rows, columns))

    def fill_random(self):
        """
        Fills the matrix with random integer values between -100 and 100.
        """
        self.data = np.random.randint(-100, 100,
                                      size=(self.rows, self.columns))

    def display(self):
        """
        Displays the matrix data.

        Prints the matrix to the console.
        """
        print(self.data)


class IntegerMatrix(Matrix):
    """
    A class that represents an integer matrix and provides methods for
    manipulating and analyzing matrix data.

    Inherits from the Matrix class.

    Attributes:
        rows (int): The number of rows in the matrix.
        columns (int): The number of columns in the matrix.
        data (numpy.ndarray): The matrix data (integer values).
    """

    def __init__(self, rows, columns):
        """
        Initializes an integer matrix with the given number of rows and
        columns.

        Args:
            rows (int): The number of rows in the matrix.
            columns (int): The number of columns in the matrix.
        """
        super().__init__(rows, columns)
        self.data = np.empty((rows, columns), dtype=int)

    def divide_by_max_abs(self):
        """
        Divides each element of the matrix by the maximum absolute value
        in the matrix. If the maximum absolute value is negative, uses the
        minimum absolute value instead.

        Updates the matrix data in place.
        """
        max_value = np.max(self.data)
        min_value = np.min(self.data)
        if abs(max_value) < abs(min_value):
            max_value = min_value
        self.data = np.divide(self.data, max_value)

    def math_variance(self):
        """
        Calculates the variance of the matrix using numpy's var function.

        Returns:
            float: The variance of the matrix, rounded to two decimal places.
        """
        variance = round(np.var(self.data), 2)
        return variance

    def custom_variance(self):
        """
        Calculates the variance of the matrix manually using the formula:
        variance = mean of squared differences from the mean.

        Returns:
            float: The variance of the matrix, rounded to two decimal places.
        """
        mean = np.mean(self.data)
        squared_diff = np.mean((self.data - mean) ** 2)
        variance = round(squared_diff, 2)
        return variance


def task5():
    """
    Handles user input and processes a matrix, displaying various operations
    like normalization and variance calculation.
    """
    m = valid_input("Enter the number of columns of the matrix: ",
                    int, 0, 10000)
    n = valid_input("Enter the number of rows of the matrix: ",
                    int, 0, 10000)

    integer_matrix = IntegerMatrix(m, n)
    integer_matrix.fill_random()
    print("Original matrix:")
    integer_matrix.display()
    integer_matrix.divide_by_max_abs()
    print()
    print("Matrix divided by the maximum absolute value:")
    integer_matrix.display()
    print()
    print("Variance using numpy:")
    print(integer_matrix.math_variance())
    print()
    print("Variance using formula:")
    print(integer_matrix.custom_variance())
