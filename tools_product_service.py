from langsmith import traceable
from langchain.tools import tool

@tool
def get_product_price(product: str) -> float:
    """Look up the price of a product in the catalog."""
    print(f"\n--> Executing @tool get_product_price (product = '{product}')")
    prices = {"laptop": 1299.99, "headphones": 149.95, "keyboard": 89.50}
    return prices.get(product, 0)


@tool
def apply_discount(price: float, discount_tier: str) -> float:
    """
    Calculate the final price after discount.
    Input 'price' MUST be the exact float returned by get_product_price.
    Input 'discount_tier' MUST be one of: 'bronze', 'silver', or 'gold'.
    """
    print(
        f"\n--> Executing @tool apply_discount (price = '{price}', discount_tier = '{discount_tier}')"
    )
    discount_percentage = {"bronze": 5, "silver": 12, "gold": 23}
    discount = discount_percentage.get(discount_tier, 0)
    return round(price * (1 - discount / 100), 2)