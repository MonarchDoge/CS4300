import sys
sys.path.append('/home/student/CS4300')

# Calculates the discount cost. only accepts whole numbers since no one uses pure decimals.
def calculate_discount(cost, discount):
    discount_percent = 1 - (discount / 100) # Get the percentage after discount subtracted ny full cost
    discounted_cost = cost * discount_percent
    return discounted_cost