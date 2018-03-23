import matplotlib.pyplot as pyplot
import re

def main():
    file = open("out.txt")
    lines = str.join("", file.readlines())

    moving_average_window = 10

    compiled = re.compile("error = (\d+.?\d*)")
    errors = list(map(float, compiled.findall(lines)))
    errors_moving_average = get_moving_average(errors, moving_average_window)

    compiled = re.compile("Actual fitness: (\d+)")
    final_scores = list(map(float, compiled.findall(lines)))
    final_scores_moving_average = get_moving_average(final_scores, moving_average_window)

    left_axes = pyplot.subplot(211)
    pyplot.ylabel("error")
    errors_plot, = left_axes.plot(errors, label="errors")
    right_axes = left_axes.twinx()
    errors_moving_average_plot, = right_axes.plot(errors_moving_average, 'y-', label="moving average")

    left_legend = pyplot.legend(handles=[errors_plot], loc=3)
    pyplot.gca().add_artist(left_legend)
    pyplot.legend(handles=[errors_moving_average_plot], loc=4)

    left_axes = pyplot.subplot(212)
    pyplot.xlabel("iteration")
    pyplot.ylabel("fitness")
    final_scores_plot, = left_axes.plot(final_scores, label="final scores")
    right_axes = left_axes.twinx()
    final_scores_moving_average_plot, = right_axes.plot(final_scores_moving_average, 'y-', label="moving average")

    left_legend = pyplot.legend(handles=[final_scores_plot], loc=3)
    pyplot.gca().add_artist(left_legend)
    pyplot.legend(handles=[final_scores_moving_average_plot], loc=4)

    pyplot.setp(errors_plot, linewidth=0.2)
    pyplot.setp(errors_moving_average_plot, linewidth=0.2)
    pyplot.setp(final_scores_plot, linewidth=0.2)
    pyplot.setp(final_scores_moving_average_plot, linewidth=0.2)

    pyplot.show()

def get_moving_average(data, window):
    moving_averages = []
    for index, datum in enumerate(data):
        if index >= window - 1:
            window_data = []
            for look_back in range(window):
                window_data.append(data[index - look_back])
            average = sum(window_data) / window
            moving_averages.append(average)
    return moving_averages

main()
