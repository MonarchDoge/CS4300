def calculate_discount(cost, discount):
    discount_percent = 1 - (discount / 100) # Get the percentage after discount
    discounted_cost = cost * discount_percent
    return discounted_cost

def test_answer():
    assert calculate_discount(100, 20) == 80
    assert calculate_discount(200, 1.5) == 197
