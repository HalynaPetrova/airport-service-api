# AIRPORT SERVICE API

The RESTful API for an airport service platform. 


## User Registration and Authentication
- Users can register with their email and password to create an account.
- Users can login with their credentials and receive a JWT token for authentication.
- Users can logout and invalidate their JWT token.

## User Profile
- Users can create and update their profile.
- Users can retrieve their own profile.

## Airport
- User with admin permission can create/update/retrieve/delete airport.
- User who is authenticated can retrieve the airport.

## Airplane type
- User with admin permission can create/update/retrieve/delete airplane type.
- The user who is authenticated can retrieve airplane type.

## Airplane
- User with admin permission can create/update/retrieve/delete airplanes.
- User who is authenticated can retrieve the airplane and filter airplanes by facilities.

## Crew
- User with admin permission can create/update/retrieve/delete crew.
- User who is authenticated can retrieve crew.

## Facility
- User with admin permission can create/update/retrieve/delete facility.
- A user who is authenticated can retrieve a facility.

## Flight
- User with admin permission can create/update/retrieve/delete flight.
- A user who is authenticated can retrieve a flight.

## Order
- Authenticated user can create/update/get/delete order, including multiple tickets in one order.

## Route
- User with admin permission can create/update/retrieve/delete routes.
- User who is authenticated can retrieve the route.

## API Permissions
- Only authenticated users can perform actions such as creating orders/tickets and adding stars to the airplane.
- User with admin permission can create/update/retrieve/delete user profile, airport, route, crew, flight, 
airplane, airplane type, tickets, order, ratings.
- Users can update their own profile.

## API Documentation
- The API is documented with clear instructions on how to use each endpoint.
- The documentation includes sample API requests and responses for different endpoints.

## Endpoint tests
  - Airport
  - AirplaneType
  - Airplane
  - Crew
  - Flight
  - Route
  - User

## How to install using GitHub
- Clone this repository
- Create venv: python -m venv venv
- Activate venv: source venv/bin/activate
- Install requirements: pip install -r requirements.txt
- Run: python manage.py runserver
- Create user via: user/register
- Get access token via: user/token

## DB structure
![airport_airplane](https://github.com/HalynaPetrova/airport-service-api/assets/92261713/0bedb93f-e46f-4b38-9e6f-696466a7a8a1)

## Pages images
![Знімок екрана з 2023-11-13 18-06-18](https://github.com/HalynaPetrova/airport-service-api/assets/92261713/a2ce2898-ca21-4f75-9cc8-96475d7f78a5)
![Знімок екрана з 2023-11-13 18-06-42](https://github.com/HalynaPetrova/airport-service-api/assets/92261713/638046b6-ae82-46b7-b93f-3cbb9e19c554)
![Знімок екрана з 2023-11-13 18-07-30](https://github.com/HalynaPetrova/airport-service-api/assets/92261713/9a9aad63-7094-487b-a409-f99c63bc5872)
![Знімок екрана з 2023-11-13 18-07-56](https://github.com/HalynaPetrova/airport-service-api/assets/92261713/881ea89d-fcb3-4577-ac26-b5d44e68e8bd)
