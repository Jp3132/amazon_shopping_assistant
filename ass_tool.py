from typing import Optional, List, Dict
import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv
import json

# Load environment variables from a .env file
load_dotenv()

# Database configuration
db_config = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_DATABASE"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

def search_product(
    name: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_rating: Optional[float] = None,
    max_rating: Optional[float] = None,
) -> str:
    """
    Search for products based on name, category, price range, and rating range.

    Args:
        name: (Optional[str]) = The name of the product. Defaults to None.
        category: (Optional[str]) = The category of the product. Defaults to None.
        min_price: (Optional[float]) = The minimum price. Defaults to None.
        max_price: (Optional[float]) = The maximum price. Defaults to None.
        min_rating: (Optional[float]) = The minimum rating. Defaults to None.
        max_rating: (Optional[float]) = The maximum rating. Defaults to None.

    Returns:
        str: A formatted string of product information matching the search criteria.
    """
    query = "SELECT product_name, discounted_price, actual_price, rating FROM amazon_products WHERE 1=1"
    params: tuple = ()

    if name:
        query += " AND LOWER(product_name) LIKE LOWER(%s)"
        params += (f"%{name}%",)
    if category:
        query += " AND LOWER(last_level_category) LIKE LOWER(%s)"
        params += (f"%{category}%",)
    if min_price is not None:
        query += " AND actual_price >= %s"
        params += (min_price,)
    if max_price is not None:
        query += " AND actual_price <= %s"
        params += (max_price,)
    if min_rating is not None:
        query += " AND rating >= %s"
        params += (min_rating,)
    if max_rating is not None:
        query += " AND rating <= %s"
        params += (max_rating,)
    query += " LIMIT 2"

    try:
        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                results = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                products = [dict(zip(columns, row)) for row in results]

        if not products:
            return "No products found matching your criteria."

        # Format the products into a string
        formatted_products = "Here are some products that match your search criteria:\n"
        for idx, product in enumerate(products, start=1):
            formatted_products += (
                f"{idx}. **{product['product_name']}**\n"
                f"   - Discounted Price: ${product['discounted_price']}\n"
                f"   - Actual Price: ${product['actual_price']}\n"
                f"   - Rating: {product['rating']} stars\n\n"
            )
        return formatted_products.strip()

    except psycopg2.Error as e:
        # Handle database errors
        print(f"Database error: {e}")
        return "Sorry, I encountered a database error while searching for products."
    except Exception as e:
        # Handle other potential errors
        print(f"An error occurred: {e}")
        return "Sorry, an unexpected error occurred while searching for products."
    

# Initialize an empty cart dictionary
cart = {}

def add_to_cart(product_id: int, product_name: str, discounted_price: float, quantity: int = 1) -> str:
    """
    Adds a product to the shopping cart or updates the quantity if it already exists.

    Args:
        product_id: (int) = The unique identifier of the product.
        product_name: (str) = The name of the product.
        discounted_price: (float) = The discounted price of the product.
        quantity: (int) = The quantity of the product to add to the cart. Defaults to 1.

    Returns:
        str: A confirmation message indicating the product has been added to the cart.
    """
    if product_id in cart:
        cart[product_id]['quantity'] += quantity
    else:
        cart[product_id] = {
            'product_name': product_name,
            'discounted_price': discounted_price,
            'quantity': quantity
        }
    return f"Added {quantity} of {product_name} to your cart."


    
def remove_from_cart(product_id: int, quantity: Optional[int] = None) -> str:
    """
    Removes a product or specified quantity from the shopping cart.

    Args:
        product_id: (int) = The unique identifier of the product.
        quantity: (Optional[int]) = The quantity to remove from the cart. If None, the product is removed entirely.

    Returns:
        str: A confirmation message indicating the product has been removed from the cart.
    """
    if product_id not in cart:
        return "Product not found in your cart."

    if quantity is None or cart[product_id]['quantity'] <= quantity:
        removed_product_name = cart[product_id]['product_name']
        del cart[product_id]
        return f"Removed {removed_product_name} from your cart."
    else:
        cart[product_id]['quantity'] -= quantity
        return f"Reduced quantity of {cart[product_id]['product_name']} by {quantity}."
    
    
def view_cart() -> str:
    """
    Retrieves and displays the contents of the shopping cart.

    Returns:
        str: A formatted string listing the products in the cart along with their quantities and prices.
    """
    if not cart:
        return "Your cart is currently empty."

    # Format the cart items into a string
    formatted_cart = "Here are the items in your cart:\n"
    for idx, (product_id, item) in enumerate(cart.items(), start=1):
        formatted_cart += (
            f"{idx}. **{item['product_name']}**\n"
            f"   - Quantity: {item['quantity']}\n"
            f"   - Price per unit: ${item['discounted_price']}\n"
            f"   - Total: ${item['discounted_price'] * item['quantity']}\n\n"
        )
    return formatted_cart.strip()

    
