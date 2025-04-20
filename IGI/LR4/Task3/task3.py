import statistics
from utils.inputs import valid_input
from .table_builder import TableBuilder
from .sequence_calculator import SequenceCalculator
from .plot_builder import PlotBuilder


def task3():
    seq = SequenceCalculator()
    series_vals = []
    while True:
        print("======================")
        choose = valid_input("Choose action:\n"
                             "0 - exit\n"
                             "1 - get results\n"
                             "2 - build plots\n", int, 0, 4)
        print("======================")
        if choose == 0:
            break
        elif choose == 1:
            eps = valid_input("Enter epsilon: ", float, 0.0)
            count = valid_input("Enter count of numbers: ", int, 0)
            raw_data = seq.generate_random_seq(count, eps)
            TableBuilder.print_table(raw_data)
            series_vals.clear()
            for row in raw_data:
                series_vals.append(row[2])

            print("\nStatistical characteristics of the sequence:")
            try:
                print(f"Mode: {statistics.mode(series_vals):.6f}")
            except statistics.StatisticsError:
                print("Mode: does not exist (all values are unique)")

            print(f"Median: {statistics.median(series_vals):.6f}")
            print(f"Mean: {statistics.mean(series_vals):.6f}")
            print(f"Variance: {statistics.variance(series_vals):.6f}")
            print("Standard deviation (SD):",
                  f"{statistics.stdev(series_vals):.6f}")
        else:
            eps = valid_input("Enter epsilon: ", float, 0.0)
            vals = seq.generate_sequence(0.01, 1, 0.01, eps)
            x_vals = []
            fx_vals = []
            fx_m_vals = []
            for val in vals:
                x_vals.append(val[0])
                fx_vals.append(val[2])
                fx_m_vals.append(val[3])
            builer = PlotBuilder(x_vals, fx_vals, fx_m_vals)
            builer.build_plot(eps)
