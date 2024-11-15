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
# Amazon Shopping Assistant CLI

## Overview

Welcome to the **Amazon Shopping Assistant CLI**! This project is a command-line interface that simulates an Amazon shopping assistant. The assistant can search for products, manage your shopping cart, assist with orders, and handle purchase queries using natural language.

The assistant leverages advanced language models to understand user queries and utilizes a PostgreSQL database to store and retrieve product and order information.

## Features

- **Search Products**: Find products based on name, category, price range, and rating.
- **Shopping Cart Management**: Add, view, and remove items from your shopping cart.
- **Checkout Process**: Proceed to checkout and place orders.
- **Order Tracking**: Check order status and estimated delivery times.
- **Payment Options**: View available payment methods.

## Prerequisites

Before running the application, ensure you have the following installed on your system:

- **Python 3.7+**
- **PostgreSQL** (for the database)
- **pip** (Python package installer)
- **virtualenv** (optional but recommended)
- **Git** (to clone the repository)

## Installation

Follow these steps to set up and run the application:

### 1. Clone the Repository

```bash
git clone <repository_url>
cd <repository_directory>