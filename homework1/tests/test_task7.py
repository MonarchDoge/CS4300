import numpy as np

# Creates an array, not stolen from my math class
def create_array(n):
    return np.arange(1, n + 1)

# Calculates the mean of the array
def calc_mean(arr):
    return np.mean(arr)

# Calculates the sum of the array
def calc_sum(arr):
    return np.sum(arr)

def test_create_array():
    arr = create_array(5)
    expected = np.array([1, 2, 3, 4, 5])
    assert np.array_equal(arr, expected)

def test_calculate_mean():
    arr = np.array([1, 2, 3, 4, 5])
    assert calc_mean(arr) == 3.0

def test_calculate_sum():
    arr = np.array([1, 2, 3, 4, 5])
    assert calc_sum(arr) == 15