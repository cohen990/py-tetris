import re


def prepare_data():
    errors, errors_moving_average = get_data_matching_regex("error = (\d+.?\d*)")
    evaluation_errors, evaluation_errors_moving_average = get_data_matching_regex("evaluation error = (\d+.?\d*)")
    final_scores, final_scores_moving_average = get_data_matching_regex("Actual fitness: (\d+)")
    evaluation_errors, final_scores = \
        truncate_to_shortest(len(errors), evaluation_errors, final_scores)
    evaluation_errors_moving_average, final_scores_moving_average = \
        truncate_to_shortest(len(errors_moving_average), evaluation_errors_moving_average, final_scores_moving_average)
    return errors, errors_moving_average, evaluation_errors, evaluation_errors_moving_average, final_scores, final_scores_moving_average


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
    moving_average_window = max(int(len(data) / 10), 1)
    moving_average = get_moving_average(data, moving_average_window)
    return data, moving_average


def truncate_to_shortest(length_of_shortest, other, another):
    other = other[:length_of_shortest]
    another = another[:length_of_shortest]
    return other, another