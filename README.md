# Airport API service

API allows users to create profiles and book flights

### The system features the following functionalities:

* JWT Authentication: Users can authenticate using JSON Web Tokens (JWT) to access protected endpoints securely.
* Admin Panel: An admin panel is available at the URL /admin/ for administrators to manage various aspects of the system.
* API Documentation: The API documentation is located at /api/doc/swagger/ and provides detailed information on available endpoints and how to use them.
* Order and Ticket Management: The system allows users to manage orders and tickets for flights. Users can book and view their flight tickets, and administrators can handle ticket-related operations.
* Flight Seat Availability: The system displays available and taken seats on flights, enabling users to choose their preferred seats during booking.
* Airport, Route, and Flight Filtering: Users can filter airports, routes, and flights based on various criteria, such as location, date, or price, to find their desired options easily.
* Administrator Rights: Administrators have special privileges to create new airports, routes, and flights, providing them with the necessary tools to manage the system effectively.

## Run docker
Docker should be installed
+ git clone https://github.com/ZaikaDaria/py-airport-api-service
+ cd py-airport-api-service
+ docker-compose up --build

## Getting access

+ create new user via /api/user/register/
+ get access token via /api/user/token/

### You can use the following test credentials:

##### Test superuser:
- Email: user@admin.com
- Password: 123456admin

##### Test user:
- Email: user@user.com
- Password: 123456user

## Configuration:
* Find the .env.sample file in the main directory of the project. This file contains the necessary variables and their expected formats, but with generic placeholder values.

* Make a copy of the .env.sample file, and then rename the duplicated file to .env. This will be the file where you will store your actual configuration values.

* Open the .env file you just created and replace the placeholder values with the specific configuration values that match your setup. These values may include sensitive information and settings needed for the project to function correctly.

By following these steps, you'll have a properly configured .env file with your custom settings, allowing the project to access the required configurations while keeping sensitive information secure.

Please remember to keep the .env file secure and avoid sharing it publicly or committing it to version control systems.