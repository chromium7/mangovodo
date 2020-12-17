# CAPSTONE: Mangovodo

### Mangovodo is an online store web application, which allows user to create an account in the store; purchase products; get a receipt; and review their purchases history.

## Project specifications and functionalities

1. User can create an account. This is implemented using django's basic authentication system.
2. Saving users' profile details, addresses and purchases. The database used here is _PostgreSQL_.
3. Asynchronously send email when user created an order. This is implemented with the use of _celery_.
4. Generate a PDF invoice of user's order information. This is done with _Weasyprint_.
5. User can perform an actual payment. _Braintree_ sandbox is used for this.
6. Updating shopping cart in every page. This is done using django context processors.
7. Recommending similar products for bundle purchase. This is implementid using _Redis_.

## How to run in development

- Install the project dependencies from requirements.txt
- Start Postgresql server
- Start Redis server
- Activate virtual environment and start celery in the project directory
- Activate virtual environment and run `python manage.py runserver`

## Explanations

The followings are the explanations for each file / folders displayed in the main directory of this repository.

- **django_projects** : This is the project directory where the settings of the project is located. It also contain celery.py file which is used to set up celery for asynchronous task. Celery is used in this project to asynchronously send email to user when the user created an order and made a payment.
- **media** : This is the directory for images uploaded by users / admins in the web app.
- **static** : This directory contains the static files for this project, collected through `python manage.py collectstatic`.
- **shop** : This first app in the project contains the core functionality of the web app. It contains the home page, product listing page, product detail page, search engine, recommender for related products and context processors.
- **coupons** : This app allows user to use a coupon for a percentage of discount off their purchases.
- **cart** : This app represents the shopping cart for the users to put their products in. The cart is available in all pages through the use of context processor.
- **orders** : The orders app will process when a user place an order / purchase. It contains the asynchronous task for celery to run and save the informations on the products purchased into Redis for scoring.
- **payment** : The payment app allows user to pay using their credit card by the use of Braintree payment gateway.
- **accounts** : The account app allows user to add or remove their registered address. User can also check the purchases that they have made, either those that haven't been paid for or those that are already completed. User can pay or cancel the orders that are still pending.

## CS50W complexity requirements:

This project is more complex than the previous projects due to the facts that it uses a lot more feature from django, including _sessions_ and _context processors_. It implements JavaScript for front-end purposes such as switching tabs in the user profile page and for sending AJAX request to Braintree server. It uses SCSS for building the CSS file for the project, so that it is easier to manage the style of the website. The project uses PostgreSQL instead of the default SQlite which provides more functionality such as the ability for a flexible search. It uses Redis which allows for giving scores to products. Admin page has more details than the previous projects, where admin can filter, do custom action such as save information as spreadsheet file, and generate PDF invoice files.

## Room for improvements:

Several concepts from CS50W were not used in this project, mainly: testing, CI/CD, scalability and security. Implementing these concepts will imply best practices, however since this is a relatively small project that was done by a single person, some concepts are deemed unnecessary.

React framework can be used for the front end of the web app, which would increase the overall responsiveness of the site and much improve the quality of the user experience.
