# 🍣 Sushi Ordering Web App

**A modern and elegant web application for online sushi ordering. Users can conveniently select dishes, specify preferences, make payments, and schedule orders for pickup at a desired time.**

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)


## Introduction

This project is a web application for sushi ordering, allowing customers to place orders online with ease. The app offers a variety of sushi options, lets customers customize their orders, and provides a simple and intuitive checkout process. It is built using Django for the backend and integrates with external payment systems to complete transactions.

## Features

Key features of the Sushi Ordering Web App include:

- **User Authentication**: Users can sign up, log in, and manage their accounts.
- **Product Listings**: Browse available sushi items and view their details, including price and ingredients.
- **Cart System**: Add products to the cart, view cart items, and modify quantities.
- **Checkout System**: Users can proceed to checkout, complete their orders, and schedule a pickup time.
- **Allergen Info**: Products include allergen information for user safety.

## Getting Started

This section will help you set up the project locally and get it running.

### Installation

Follow these steps to install and run the project locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/ntkachenko21/sushi-store.git
   
2. Navigate to the project directory:
   ```bash
   cd sushi-store

3. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   
5. Run database migrations:
   ```bash
   python manage.py migrate
   
6. Start the development server:
   ```bash
   python manage.py runserver

This will set up and run the development server. You can now access the app at http://127.0.0.1:8000/.

Load Fixtures (Optional)
Fixtures are used to populate your database with initial data such as products, categories, and other necessary records. To load a fixture, follow these steps:

1. Ensure the server is stopped, if running.

2. In the root of the project directory, run the following command to load the fixture:
   ```bash
   python manage.py loaddata massive_product_fixture.json

This will populate your database with the initial data from the fixture file.
