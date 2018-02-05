import hybrid_output as log
import numpy as np

class AssertionException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

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
