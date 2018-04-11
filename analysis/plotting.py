from matplotlib import pyplot, pyplot as pyplot


def plot_scores(left_axes, right_axes, scores, moving_average):
    scores_plot, = left_axes.plot(scores, label="final scores")
    moving_average_plot, = right_axes.plot(moving_average, 'y-', label="moving average")
    pyplot.setp(scores_plot, linewidth=0.2, color="blue")
    pyplot.setp(moving_average_plot, linewidth=0.2, color="orange")
    left_legend = pyplot.legend(handles=[scores_plot], loc=3)
    pyplot.gca().add_artist(left_legend)
    pyplot.legend(handles=[moving_average_plot], loc=4)


def plot_evaluations(evaluation, moving_average, left_axes, right_axes):
    evaluation_plot, = left_axes.plot(evaluation, label="evaluation")
    moving_average_plot, = right_axes.plot(moving_average, 'y-', label="average evaluation")

    pyplot.setp(evaluation_plot, linewidth=0.3, color="yellow", alpha=0.5)
    pyplot.setp(moving_average_plot, linewidth=0.3, color="orange")
    left_legend = pyplot.legend(handles=[evaluation_plot], loc=3)
    pyplot.gca().add_artist(left_legend)
    pyplot.legend(handles=[moving_average_plot], loc=4)


def plot_errors(errors, moving_average, left_axes, right_axes):
    errors_plot, = left_axes.plot(errors, label="errors")
    moving_average_plot, = right_axes.plot(moving_average, 'y-', label="average error")
    pyplot.setp(errors_plot, linewidth=0.2, color="blue")
    pyplot.setp(moving_average_plot, linewidth=0.3, color="purple")
    left_legend = pyplot.legend(handles=[errors_plot], loc=3)
    pyplot.gca().add_artist(left_legend)
    pyplot.legend(handles=[moving_average_plot], loc=4)


def clear_all_subplots(bottom_left_axes, bottom_right_axes, top_left_axes, top_right_axes):
    top_left_axes.clear()
    top_right_axes.clear()
    bottom_left_axes.clear()
    bottom_right_axes.clear()


def prepare_subplots():
    top_left_axes = pyplot.subplot(211)
    top_right_axes = top_left_axes.twinx()
    bottom_left_axes = pyplot.subplot(212)
    bottom_right_axes = bottom_left_axes.twinx()
    return bottom_left_axes, bottom_right_axes, top_left_axes, top_right_axes


def draw_all(bottom_left_axes, bottom_right_axes, top_left_axes, top_right_axes):
    top_left_axes.plot()
    top_right_axes.plot()
    bottom_left_axes.plot()
    bottom_right_axes.plot()