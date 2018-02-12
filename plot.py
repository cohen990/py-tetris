import matplotlib.pyplot as pyplot
import re

def main():
    file = open("out.txt")
    lines = str.join("", file.readlines())

    moving_average_window = 100

    compiled = re.compile("error = (\d+.?\d*)")
    errors = list(map(float, compiled.findall(lines)))
    errors_moving_average = get_moving_average(errors, moving_average_window)

    compiled = re.compile("Actual fitness: (\d+)")
    final_scores = list(map(float, compiled.findall(lines)))
    final_scores_moving_average = get_moving_average(final_scores, moving_average_window)

    pyplot.subplot(211)
    pyplot.plot(errors)
    pyplot.plot(errors_moving_average)
    pyplot.xlabel("iteration")
    pyplot.ylabel("error")

    pyplot.subplot(212)
    pyplot.plot(final_scores)
    pyplot.plot(final_scores_moving_average)
    pyplot.xlabel("iteration")
    pyplot.ylabel("fitness")
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
