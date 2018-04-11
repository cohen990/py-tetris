import matplotlib.pyplot as pyplot
import matplotlib.animation as animation
import re

figure = pyplot.figure()
def animate():
    initial_errors, initial_errors_moving_average = get_data_matching_regex("initial error = (\d+.?\d*)")
    final_errors, final_errors_moving_average = get_data_matching_regex("final error = (\d+.?\d*)")
    evaluation_errors, evaluation_errors_moving_average = get_data_matching_regex("evaluation error = (\d+.?\d*)")
    final_scores, final_scores_moving_average = get_data_matching_regex("Actual fitness: (\d+)")

    left_axes = pyplot.subplot(211)
    pyplot.ylabel("error")
    initial_errors_plot, = left_axes.plot(initial_errors, label="errors")
    final_errors_plot, = left_axes.plot(final_errors, label="errors")
    evaluation_errors_plot, = left_axes.plot(evaluation_errors, label="errors")
    right_axes = left_axes.twinx()
    initial_errors_moving_average_plot, = right_axes.plot(initial_errors_moving_average, 'y-', label="moving average")
    final_errors_moving_average_plot, = right_axes.plot(final_errors_moving_average, 'y-', label="moving average")
    evaluation_errors_moving_average_plot, = right_axes.plot(evaluation_errors_moving_average, 'y-', label="moving average")
    right_axes.fill_between(range(len(initial_errors_moving_average)), initial_errors_moving_average, final_errors_moving_average, alpha=0.7)

    left_legend = pyplot.legend(handles=[final_errors_plot], loc=3)
    pyplot.gca().add_artist(left_legend)
    pyplot.legend(handles=[final_errors_moving_average_plot], loc=4)

    left_axes = pyplot.subplot(212)
    pyplot.xlabel("iteration")
    pyplot.ylabel("fitness")
    final_scores_plot, = left_axes.plot(final_scores, label="final scores")
    right_axes = left_axes.twinx()
    final_scores_moving_average_plot, = right_axes.plot(final_scores_moving_average, 'y-', label="moving average")

    left_legend = pyplot.legend(handles=[final_scores_plot], loc=3)
    pyplot.gca().add_artist(left_legend)
    pyplot.legend(handles=[final_scores_moving_average_plot], loc=4)

    pyplot.setp(initial_errors_plot, linewidth=0.2)
    pyplot.setp(initial_errors_moving_average_plot, linewidth=0.3)
    pyplot.setp(final_errors_plot, linewidth=0.2)
    pyplot.setp(final_errors_moving_average_plot, linewidth=0.3)
    pyplot.setp(evaluation_errors_plot, linewidth=0.3, color="blue", alpha=0.5)
    pyplot.setp(evaluation_errors_moving_average_plot, linewidth=0.3, color="blue")
    pyplot.setp(final_scores_plot, linewidth=0.2)
    pyplot.setp(final_scores_moving_average_plot, linewidth=0.2)

    pyplot.savefig('plot.png')
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

def get_data_matching_regex(regex):
    file = open("out.txt")
    lines = str.join("", file.readlines())

    compiled = re.compile(regex)
    data = list(map(float, compiled.findall(lines)))
    moving_average_window = max(int(len(data)/10), 1)
    moving_average = get_moving_average(data, moving_average_window)
    return data, moving_average

animated_plot = animation.FuncAnimation(figure, animate, interval=1000)
pyplot.show()
