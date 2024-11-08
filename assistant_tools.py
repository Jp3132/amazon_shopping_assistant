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
def search_products(
    name: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_rating: Optional[float] = None,
    max_rating: Optional[float] = None,
) -> List[Dict]:
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
        List[Dict]: A list of product dictionaries matching the search criteria.
    """
    # Ensure db_config is defined appropriately
    # db_config should be a dictionary with keys like 'dbname', 'user', etc.
    # Example:
    # db_config = {
    #     'dbname': 'your_db',
    #     'user': 'your_username',
    #     'password': 'your_password',
    #     'host': 'localhost',
    #     'port': 5432
    # }

    query = "SELECT product_name,discounted_price,actual_price,rating FROM amazon_products WHERE 1=1"
    params: Tuple = ()

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
                return [dict(zip(columns, row)) for row in results]
    except psycopg2.Error as e:
        # Handle database errors
        print(f"Database error: {e}")
        return []
    except Exception as e:
        # Handle other potential errors
        print(f"An error occurred: {e}")
        return []