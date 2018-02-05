import hybrid_output as log
import numpy as np
import evaluator
import inspect
from test_framework import AssertionException

def run_test(test_name, test_method):
    test_passed = True
    test_status = "PASS"
    log.write("> ", test_name)
    try:
        test_method()
    except AssertionException as error:
        test_passed = False
        test_status = "FAIL"
        test_status += "\n"
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

members = inspect.getmembers(evaluator)
results = []
for member in members:
    subMemberNames = dir(member[1])
    is_test = "is_test" in subMemberNames and not member[0] == "evaluator"
    if is_test:
        results.append(run_test(member[0], member[1]))
output_results(results)
