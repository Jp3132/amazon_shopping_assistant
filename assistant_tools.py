# #Tool Name	Purpose	Inputs	Example Use Cases
# ProductSearchTool	Handle product search and specifications	query, filters	Search products by category, fetch product details, filter by price/brand
# RecommendationTool	Suggest related or alternative products	product_id, context	Recommend similar items, suggest popular products, personalize based on preferences
# CartManagementTool	Manage shopping cart actions	action, product_id, quantity	Add/remove items, view cart summary, confirm cart actions
# OrderQueryTool	Handle order and checkout queries	query_type, order_id



# class tools():
#     """
#     A single class that contains all tools for product search, recommendations,
#     cart management, and order queries.
#     """

#     def __init__(self, db_config):
#         """
#         Initialize with database configuration and set up an in-memory cart.
        
#         :param db_config: Dictionary containing connection details
#         """
#         self.db_config = db_config
#         self.cart = {}

#     def connect(self):
#         """
#         Establish a connection to the database using provided config.
#         """
#         return psycopg2.connect(**self.db_config)

    # Product Search Tool
    
    # def search_products(self, query, filters={}):
    #     """
    #     Search for products based on query and optional filters.

    #     :param query: Search term (e.g., "smartphone")
    #     :param filters: Additional filters like price, category, or brand
    #     :return: List of matching products
    #     """
    #     base_query = "SELECT product_id, product_name, discounted_price, actual_price, rating, about_product FROM products WHERE LOWER(product_name) LIKE %s"
    #     params = [f"%{query.lower()}%"]

    #     # Add filters if specified
    #     if 'price' in filters:
    #         base_query += " AND discounted_price <= %s"
    #         params.append(filters['price'])
    #     if 'category' in filters:
    #         base_query += " AND LOWER(category) = %s"
    #         params.append(filters['category'].lower())

    #     with self.connect() as conn:
    #         with conn.cursor() as cursor:
    #             cursor.execute(base_query, tuple(params))
    #             results = cursor.fetchall()

    #     # Format the results
    #     products = [{"product_id": row[0], "name": row[1], "discounted_price": row[2], "actual_price": row[3], "rating": row[4], "about": row[5]} for row in results]
    #     return products
    

import os
from dotenv import load_dotenv

load_dotenv()
db_config = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "database": os.getenv("DB_DATABASE"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

# def search_products(
#     name: Optional[str] = None,
#     category: Optional[str] = None,
#     price_range: Optional[tuple] = None,
# ) -> str:
#     """
#     Search for products based on name, category, and price range.

#     Args:
#         name: Optional[str] = The name of the product to search for. Defaults to None.
#         category: Optional[str] = The category of the product. Defaults to None.
#         price_range: Optional[tuple] = A tuple with minimum and maximum price as (min_price, max_price). Defaults to None.

#     Returns:
#         List[dict]: A list of product dictionaries matching the search criteria.
#     """
#     # Connect to the SQLite database (replace with your database path or connection string)
#     conn = psycopg2.connect(db_config)
#     cursor = conn.cursor()

#     # Base query to select products
#     query = "SELECT * FROM products WHERE 1=1"
#     params = []

#     # Search by product name
#     if name:
#         query += " AND name LIKE ?"
#         params.append(f"%{name}%")

#     # Filter by category
#     if category:
#         query += " AND category LIKE ?"
#         params.append(f"%{category}%")

#     # Filter by price range
#     if price_range:
#         min_price, max_price = price_range
#         if min_price is not None:
#             query += " AND discounted_price >= ?"
#             params.append(min_price)
#         if max_price is not None:
#             query += " AND discounted_price <= ?"
#             params.append(max_price)

#     # Execute the query and fetch results
#     cursor.execute(query, params)
#     results = cursor.fetchall()

#     # Close the connection
#     conn.close()

#     # Return results as a list of dictionaries
#     return json.dumps([
#         dict(zip([column[0] for column in cursor.description], row)) for row in results
#     ])



import psycopg2
from datetime import datetime
from typing import Optional, Union, List, Dict, Tuple
import json
# def search_products(
#     name: Optional[str] = None,
#     category: Optional[str] = None,
#     min_price: Optional[float] = None,
#     max_price: Optional[float] = None,
#     min_rating: Optional[float] = None,
#     max_rating: Optional[float] = None,
# ) -> List[Dict]:
#     """
#     Search for products based on name, category, price range, and rating range.

#     Args:
#         name: (Optional[str]) = The name of the product. Defaults to None.
#         category: (Optional[str]) = The category of the product. Defaults to None.
#         min_price: (Optional[float]) = The minimum price. Defaults to None.
#         max_price: (Optional[float]) = The maximum price. Defaults to None.
#         min_rating: (Optional[float]) = The minimum rating. Defaults to None.
#         max_rating: (Optional[float]) = The maximum rating. Defaults to None.

#     Returns:
#         List[Dict]: A list of product dictionaries matching the search criteria.
#     """
#     # Ensure db_config is defined appropriately
#     # db_config should be a dictionary with keys like 'dbname', 'user', etc.
#     # Example:
#     # db_config = {
#     #     'dbname': 'your_db',
#     #     'user': 'your_username',
#     #     'password': 'your_password',
#     #     'host': 'localhost',
#     #     'port': 5432
#     # }

#     query = "SELECT product_name,discounted_price,actual_price,rating FROM amazon_products WHERE 1=1"
#     params: Tuple = ()

#     if name:
#         query += " AND LOWER(product_name) LIKE LOWER(%s)"
#         params += (f"%{name}%",)
#     if category:
#         query += " AND LOWER(last_level_category) LIKE LOWER(%s)"
#         params += (f"%{category}%",)
#     if min_price is not None:
#         query += " AND actual_price >= %s"
#         params += (min_price,)
#     if max_price is not None:
#         query += " AND actual_price <= %s"
#         params += (max_price,)
#     if min_rating is not None:
#         query += " AND rating >= %s"
#         params += (min_rating,)
#     if max_rating is not None:
#         query += " AND rating <= %s"
#         params += (max_rating,)
#     query += " LIMIT 2"
#     try:
#         with psycopg2.connect(**db_config) as conn:
#             with conn.cursor() as cursor:
#                 cursor.execute(query, params)
#                 results = cursor.fetchall()
#                 columns = [desc[0] for desc in cursor.description]
#                 return [dict(zip(columns, row)) for row in results]
#     except psycopg2.Error as e:
#         # Handle database errors
#         print(f"Database error: {e}")
#         return []
#     except Exception as e:
#         # Handle other potential errors
#         print(f"An error occurred: {e}")
#         return []

from typing import Optional
import psycopg2
from psycopg2 import sql
from decimal import Decimal

def search_products(
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
        str: A formatted string of products matching the search criteria or a message indicating no results.
    """
    # Ensure db_config is defined appropriately
    db_config = {
        'host': os.getenv("DB_HOST"),
        'port': os.getenv("DB_PORT"),
        'dbname': os.getenv("DB_DATABASE"),
        'user': os.getenv("DB_USER"),
        'password': os.getenv("DB_PASSWORD")
    }

    query = "SELECT product_name, discounted_price, actual_price, rating, product_id FROM amazon_products WHERE 1=1"
    params = []

    if name:
        query += " AND LOWER(product_name) LIKE LOWER(%s)"
        params.append(f"%{name}%")
    if category:
        query += " AND LOWER(last_level_category) LIKE LOWER(%s)"
        params.append(f"%{category}%")
    if min_price is not None:
        query += " AND actual_price >= %s"
        params.append(min_price)
    if max_price is not None:
        query += " AND actual_price <= %s"
        params.append(max_price)
    if min_rating is not None:
        query += " AND rating >= %s"
        params.append(min_rating)
    if max_rating is not None:
        query += " AND rating <= %s"
        params.append(max_rating)
    query += " LIMIT 3"

    try:
        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, tuple(params))
                results = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]

                if not results:
                    return "No products found for the specified criteria."

                # Format the results into a readable string
                product_list = "\n\n".join([
                    f"{i+1}. {row[0]}\n   Price: ₹{row[1]} (Discounted), ₹{row[2]} (Actual)\n   Rating: {row[3]}, Product_id: {row[4]}"
                    for i, row in enumerate(results)
                ])
                return product_list

    except psycopg2.Error as e:
        # Handle database errors
        print(f"Database error: {e}")
        return "An error occurred while searching for products."
    except Exception as e:
        # Handle other potential errors
        print(f"An unexpected error occurred: {e}")
        return "An unexpected error occurred while processing your request."


def add_to_cart(product_id: str, product_name: str, discounted_price: float, quantity: int = 1) -> str:
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


    
def remove_from_cart(product_id: str, quantity: Optional[int] = None) -> str:
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
        str: A formatted string listing the products in the cart along with their quantities, prices, and grand total.
    """
    if not cart:
        return "Your cart is currently empty."

    # Initialize formatted string and grand total
    formatted_cart = "Here are the items in your cart:\n"
    grand_total = 0

    # Format each item in the cart
    for idx, (product_id, item) in enumerate(cart.items(), start=1):
        item_total = item['discounted_price'] * item['quantity']  # Calculate total for each item
        grand_total += item_total  # Accumulate to grand total

        # Format each item with two decimal places for prices
        formatted_cart += (
            f"{idx}. **{item['product_name']}**\n"
            f"   - Quantity: {item['quantity']}\n"
            f"   - Price per unit: ₹{item['discounted_price']:.2f}\n"
            f"   - Total: ₹{item_total:.2f}\n\n"
        )

    # Append grand total to the formatted cart
    formatted_cart += f"Grand Total: ₹{grand_total:.2f}"
    return formatted_cart.strip() 
    
# def view_cart() -> str:
#     """
#     Retrieves and displays the contents of the shopping cart.

#     Returns:
#         str: A formatted string listing the products in the cart along with their quantities and prices.
#     """
#     if not cart:
#         return "Your cart is currently empty."

#     # Format the cart items into a string
#     formatted_cart = "Here are the items in your cart:\n"
#     for idx, (product_id, item) in enumerate(cart.items(), start=1):
#         formatted_cart += (
#             f"{idx}. **{item['product_name']}**\n"
#             f"   - Quantity: {item['quantity']}\n"
#             f"   - Price per unit: ${item['discounted_price']}\n"
#             f"   - Total: ${item['discounted_price'] * item['quantity']}\n\n"
#         )
#     return formatted_cart.strip()


from datetime import datetime, timedelta
import json
cart ={}
def checkout(user_id: int) -> str:
    """
    Processes checkout by creating an order in the database with items from the cart.
    Clears the cart after successful checkout.

    Args:
        user_id: (int) = The ID of the user checking out.

    Returns:
        str: Confirmation message with the order details and estimated delivery time.
    """
    if not cart:
        return "Your cart is empty. Add items to your cart before proceeding to checkout."

    order_date = datetime.now()
    delivery_date = order_date + timedelta(days=7)  # Assuming a standard delivery time of 7 days

    try:
        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                # Insert each item in the cart as a separate row in the orders table
                for product_id, item in cart.items():
                    total_price = item['discounted_price'] * item['quantity']
                    cursor.execute(
                        """
                        INSERT INTO orders (user_id, product_id, quantity, order_date, total_price, 
                                            order_status, delivery_date)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        RETURNING order_id
                        """,
                        (user_id, product_id, item['quantity'], order_date, total_price, 'Processing', delivery_date)
                    )
                    order_id = cursor.fetchone()[0]  # Fetch the order ID for confirmation

                conn.commit()
        sum_1 = sum(item['discounted_price'] * item['quantity'] for item in cart.values())
        # Clear the cart after checkout
        cart.clear()

        return (f"Order(s) have been placed successfully with a total of ₹{sum_1:.2f}. "
                f"All items are now being processed and will be delivered by {delivery_date.strftime('%Y-%m-%d')}.")
    
    except Exception as e:
        return f"An error occurred during checkout: {e}"

def get_delivery_time(order_id: int) -> str:
    """
    Retrieves the delivery time for a specific order from the database.

    Args:
        order_id: (int)= The ID of the order.

    Returns:
        str: The estimated delivery date for the order.
    """
    try:
        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT delivery_date FROM orders WHERE order_id = %s", (order_id,))
                result = cursor.fetchone()
                if result and result[0]:
                    return f"The estimated delivery date for order #{order_id} is {result[0]}."
                else:
                    return f"Delivery date for order #{order_id} is not yet available."
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return "An error occurred while retrieving the delivery time."
    
def get_payment_options() -> str:
    """
    Provides available payment options.

    Returns:
        str: Payment options information.
    """
    return "We accept major credit cards, debit cards, PayPal, and Amazon Pay."

def get_order_status(order_id: int) -> str:
    """
    Retrieves the current status of an order from the database.

    Args:
        order_id: (int)= The ID of the order.

    Returns:
        str: The current status of the specified order.
    """
    try:
        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT order_status FROM orders WHERE order_id = %s", (order_id,))
                result = cursor.fetchone()
                if result:
                    return f"The status of order #{order_id} is '{result[0]}'."
                else:
                    return f"Order #{order_id} not found."
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return "An error occurred while retrieving the order status."