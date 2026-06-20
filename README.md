# Ticket API - Techinical test
The purpose of this project is to demonstrate how a simple back-end for a Ticket system works.

In this project you are able to utilize the admin user to create Customers and Attendants that will be able to interact with the system utilizing the API routes and tokens.

The Customer profile enable the users to create new tickets, view and update information about the tickets that they have created, as well as post interaction messages to communicate with the Attendants.

The Attendant profile are responsable for manage the Ticket categories, as well as view all of the created tickets, set itself or another user as responsable for a specific ticket, update the ticket status, and interact on the tickets posting messages to communicate with the clients.

## Installation
To run this project localy, it's recomended to have the [Docker Compose](https://docs.docker.com/compose/install/) installed, either using Docker Desktop or the Docker CLI.

On the docker-compose.yml file you can setup the local variables needed to setup your environment locally, or in a remote server.

Everything that you need to setup your application is ready to use on the Docker, docker-compose.yml and django.sh files, you only need to toggle some environment variables (i.e.: MOCK_DATA) to decide if the database will be pupulated with the full mock data or not.

After checking your variables on the docker-compose.yml file, you just need to run in your terminal

    docker compose up -d --build --remove-orphans
*IMPORTANT - Don't forget to run this command on the same folder as the Docker file inside this project*

After this, you can access [http://localhost:8000/admin/](http://localhost:8000/admin/) to manage your users, or the [http://localhost:8000/api/](http://localhost:8000/api/) to access your application.

To see the full API documentation you can either:
  - Access the swagger-ui on [http://localhost:8000/api/schema/swagger-ui](http://localhost:8000/api/schema/swagger-ui)
  - Access the redoc on [http://localhost:8000/api/schema/redoc](http://localhost:8000/api/schema/redoc)

## Development and local tests
If you want to make some changes on this simple API, on the file ticketapi/tests.py there is a list of unit tests ready to use, you just need to execute the following command on the root folder in your terminal:

    python .\manage.py test

*If you extend the API with new endpoints, or have made some changes in the data structure, don't forget to update the tests file!*

This project has a github-action workflow implemented on the .github\worflows folder, executing the unit tests before deploy on a Cloud Oracle instance.

You can implement your CI/CD worflow on any platform that you feel confortable, as long as you don't forget to setup your environment variables, and check if the platform is compatible with Docker Compose, or only simple Docker containers with a separated database location.

The full list of environment variables that you need to deploy is:

    # Ticket API variables
    PG_USER=postgres #your database user - must be the same as $POSTGRES_USER 
    PG_PASSWORD=postgres #your database password - must be the same as $POSTGRES_PASSWORD
    PG_DB=postgres #your database name - must be the same as $POSTGRES_DB
    PG_HOST=db #the ip addres of your server - db if it's managed by composer
    PG_PORT=5432 #your postgree db port
    SECRET_KEY='django-hash-key' #the secret key for your django application
    DEBUG=False #django Debug status
    MOCK_DATA=true #populate your database with mock users/tickets/interactions
    # Postgree database variables
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_DB=postgres
