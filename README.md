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
![airport_airplane.png](..%2F..%2F%D0%97%D0%BE%D0%B1%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%BD%D1%8F%2Fairport_airplane.png)

## Pages images
![Знімок екрана з 2023-11-13 18-06-18.png](..%2F..%2F%D0%97%D0%BE%D0%B1%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%BD%D1%8F%2F%D0%97%D0%BD%D1%96%D0%BC%D0%BA%D0%B8%20%D0%B5%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%2F%D0%97%D0%BD%D1%96%D0%BC%D0%BE%D0%BA%20%D0%B5%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%20%D0%B7%202023-11-13%2018-06-18.png)
![Знімок екрана з 2023-11-13 18-06-42.png](..%2F..%2F%D0%97%D0%BE%D0%B1%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%BD%D1%8F%2F%D0%97%D0%BD%D1%96%D0%BC%D0%BA%D0%B8%20%D0%B5%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%2F%D0%97%D0%BD%D1%96%D0%BC%D0%BE%D0%BA%20%D0%B5%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%20%D0%B7%202023-11-13%2018-06-42.png)
![Знімок екрана з 2023-11-13 18-07-30.png](..%2F..%2F%D0%97%D0%BE%D0%B1%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%BD%D1%8F%2F%D0%97%D0%BD%D1%96%D0%BC%D0%BA%D0%B8%20%D0%B5%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%2F%D0%97%D0%BD%D1%96%D0%BC%D0%BE%D0%BA%20%D0%B5%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%20%D0%B7%202023-11-13%2018-07-30.png)
![Знімок екрана з 2023-11-13 18-07-56.png](..%2F..%2F%D0%97%D0%BE%D0%B1%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%BD%D1%8F%2F%D0%97%D0%BD%D1%96%D0%BC%D0%BA%D0%B8%20%D0%B5%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%2F%D0%97%D0%BD%D1%96%D0%BC%D0%BE%D0%BA%20%D0%B5%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%20%D0%B7%202023-11-13%2018-07-56.png)
