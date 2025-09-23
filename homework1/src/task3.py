import sys
sys.path.append('/home/student/CS4300')

# Basic if statement that checks for 0's and negative numbers. Everything else is positive
def pos_neg_checker(x):
    Type = ""
    if x == 0:
        Type = "Zero"
    elif x < 0:
        Type = "Negative"
    else:
        Type = "Positive"
    return Type

# Checks for Prime Numbers
def first_primes():
    n = 2
    primes = []
    while len(primes)<10:
        if prime_numbers(n):
            primes.append(n)
        n += 1
    return primes

# Checks if a number is prime
def prime_numbers(n):
    flag = True
    if n <= 1:
        flag = False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            flag = False
    return flag


# Adds up the first 100 numbers.
def summation_of_100():
    n = 1
    total = 0
    while n <= 100:
        total += n
        n += 1
    return n

