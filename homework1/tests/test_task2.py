# Integer adding
def int_use(x):
    return x + 3

# Subtracting a float from an int or a float returns a float
def float_use(x):
    return x - 1.1

# adding strings together creates a larger string
def string_use(x, y):
    return (x + y)

# Just bool things
def bool_use(x):
    return(x)

def test_answer():
    assert int_use(5) == 8 
    assert int_use(-2) == 1
    assert int_use(-10) == -7


def float_test_answer():
    assert float_use(3) == 1.9

def string_test_answer():
    assert string_use("Hello", " World!") == "Hello World!"
    assert string_use("Goodbye", " World!") == "Goodbye World!"
    assert string_use("String", " Combining") == "String Combining"

def bool_test_use():
    assert bool_use(True) == True