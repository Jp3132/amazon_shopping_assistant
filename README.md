Amazon Shopping Assistant CLI

An Amazon-like shopping assistant that allows users to search for products, manage their shopping cart, and place orders via a command-line interface, using a language model to handle user interactions.

Description

This project implements a command-line interface (CLI) for an Amazon Shopping Assistant. Users can interact with the assistant to search for products, add or remove items from their cart, view the cart, and proceed to checkout. The assistant uses a language model to interpret user inputs and provide appropriate responses, leveraging tools to perform actions such as database queries and cart management.

The assistant is built using langchain, langgraph, and groq, and connects to a PostgreSQL database to retrieve product information and manage orders.

Features

	•	Search for products by name, category, price range, and rating.
	•	Add products to the shopping cart.
	•	Remove products from the shopping cart.
	•	View the contents of the shopping cart.
	•	Checkout and place orders.
	•	Get payment options.
	•	Check order status.
	•	Get estimated delivery times.

Installation

Prerequisites

	•	Python 3.7 or higher
	•	PostgreSQL database with the necessary tables and data
	•	Git (to clone the repository)
