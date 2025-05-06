import matplotlib.pyplot as plt


class PlotBuilder:
    """
    Class to build and display a plot comparing the natural log function and
    its Taylor series approximation.
    """
    def __init__(self, x_vals, fx_vals, fx_m_vals):
        """
        Initializes the PlotBuilder with x values, function values, and Taylor
        series values.

        Args:
            x_vals (list): x values for plotting.
            fx_vals (list): Taylor series approximation values.
            fx_m_vals (list): function values (ln(1 + x)) for comparison.
        """
        self._x_vals = x_vals
        self._fx_vals = fx_vals
        self._fx_m_vals = fx_m_vals

    def build_plot(self, eps):
        """
        Builds and displays a plot comparing the natural log function and its
        Taylor series approximation.

        Args:
            eps (float): The epsilon value used in the Taylor series
            approximation for labeling.
        """
        plt.figure(figsize=(10, 6))
        plt.plot(self._x_vals, self._fx_m_vals, label="ln(1 + x)",
                 color="black", linestyle="--", linewidth=2)
        plt.plot(self._x_vals, self._fx_vals,
                 label=f"Taylor series (eps={eps})", color="blue")

        plt.title("Comparison: ln(1 + x) vs Taylor Series Approximation")
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.legend()
        plt.annotate(
            'Annotation',
            xy=(0, 0),     
            xytext=(10, 0),
            textcoords='offset points'
        )
        plt.grid(True)
        plt.xlim(0, 1)
        plt.savefig("Task3/plots.png")
        plt.show()
