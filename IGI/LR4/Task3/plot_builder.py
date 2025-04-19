import matplotlib.pyplot as plt


class plot_builder:
    def __init__(self, x_vals, fx_vals, fx_m_vals):
        self._x_vals = x_vals
        self._fx_vals = fx_vals
        self._fx_m_vals = fx_m_vals

    def build_plot(self, eps):
        plt.figure(figsize=(10, 6))
        plt.plot(self._x_vals, self._fx_m_vals, label="ln(1 + x) [math.log]",
                 color="black", linestyle="--", linewidth=2)
        plt.plot(self._x_vals, self._fx_vals,
                 label=f"Taylor series (eps={eps})", color="blue")

        plt.title("Comparison: ln(1 + x) vs Taylor Series Approximation")
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.legend()
        plt.grid(True)
        plt.xlim(0, 1)
        plt.savefig("Task3/plots.png")
        plt.show()
