import matplotlib.pyplot as pyplot
import matplotlib.animation as animation

from analysis.data import prepare_data
from analysis.plotting import plot_scores, plot_evaluations, plot_errors, clear_all_subplots, prepare_subplots, draw_all

figure = pyplot.figure()


def animate(_):
    errors, errors_moving_average, evaluations, evaluation_moving_average, final_scores, final_scores_moving_average,\
        = prepare_data()

    bottom_left_axes, bottom_right_axes, top_left_axes, top_right_axes = prepare_subplots()
    clear_all_subplots(bottom_left_axes, bottom_right_axes, top_left_axes, top_right_axes)

    pyplot.ylabel("error")
    plot_errors(errors, errors_moving_average, top_left_axes, top_right_axes)
    plot_evaluations(evaluations, evaluation_moving_average, top_left_axes, top_right_axes)

    pyplot.xlabel("iteration")
    pyplot.ylabel("fitness")
    plot_scores(bottom_left_axes, bottom_right_axes, final_scores, final_scores_moving_average)
    draw_all(bottom_left_axes, bottom_right_axes, top_left_axes, top_right_axes)


seconds = 1000
animated_plot = animation.FuncAnimation(figure, animate, interval=(600 * seconds))
pyplot.show()
