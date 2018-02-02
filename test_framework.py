import hybrid_output as log
import numpy as np
import evaluator
import inspect

class AssertionException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

def run_test(test_name, test_method):
    test_passed = True
    test_status = "PASS"
    log.write("> ", test_name)
    try:
        test_method()
    except AssertionException as error:
        test_passed = False
        test_status = "FAIL"
        test_status += ": "
        test_status += str(error)
    log.write(test_status)
    return test_passed

def output_results(results):
    log.write("Test run complete. Ran " + str(len(results)) + " tests")
    output_successes(results)
    output_failures(results)

def output_successes(results):
    log.write(str(get_count_matching(results, True)) + " passed")

def output_failures(results):
    log.write(str(get_count_matching(results, False)) + " failed")

def get_count_matching(array, to_match):
    indices = [i for i, x in enumerate(array) if x == to_match]
    return(len(indices))

def assert_true(conditional):
    if not conditional:
        raise AssertionException("Expected True. Was False")

def assert_arrays_equal(array1, array2):
    passed = np.array_equal(array1, array2)
    if not passed:
        message = ""
        message += ">>>>The two arrays were not equal\n"
        message += str(array1)
        message += "\n"
        message += str(array2)
        message += "\n"
        message += "<<<<"
        raise AssertionException(message)

def test(func):
    func.is_test = True
    return func

members = inspect.getmembers(evaluator)
results = []
for member in members:
    subMemberNames = dir(member[1])
    is_test = "is_test" in subMemberNames and not member[0] == "evaluator"
    if is_test:
        results.append(run_test(member[0], member[1]))
output_results(results)
