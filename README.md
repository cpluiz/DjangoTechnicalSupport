# Ticket API - Technical Test

This project demonstrates a simple, robust backend for a ticketing system built with Django and Python. 

Admin users can manage the platform, while Customers and Attendants interact through secure API routes using authentication tokens.

## 1. Project Purpose
The purpose of this project is to showcase a functional ticketing system backend. It implements distinct user roles, automated database population, comprehensive unit testing, and a complete CI/CD pipeline to simulate a real-world production deployment.

## 2. Technologies Used
* **Python** - Core programming language.
* **Django & Django REST Framework** - Web framework and API toolkit.
* **PostgreSQL** - Production-grade relational database.
* **Docker & Docker Compose** - Containerization and local environment orchestration.
* **GitHub Actions** - Continuous Integration and Continuous Deployment runner.
* **Swagger UI & ReDoc** - Interactive API documentation tools.

## 3. How to Run the Project Locally (Without Docker)
If you prefer to run the application directly on your host machine, follow these steps:

### Step 1: Clone and Set Up the Environment
1. **Clone the repository** and navigate to the root directory:
   ```bash
   git clone git@github.com:cpluiz/DjangoTechnicalSupport.git
   cd DjangoTechnicalSupport
   ```
2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: .\venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Step 2: Database Setup & Configuration
Before starting the application locally, you must provide a functional PostgreSQL instance:
1. Ensure you have a local **PostgreSQL instance** installed and running.
2. Create a database instance matching your intended environment variable config:
   ```sql
   CREATE DATABASE postgres;
   ```
3. Create a local `.env` file in the root project folder matching your target server parameters. Make sure `PG_HOST` is explicitly set to `localhost` or `127.0.0.1` for local mapping (see the **Environment Variables Configuration** section below).

### Step 3: Run Database Init & Server
1. **Apply migrations** manually to build the database schema structure:
   ```bash
   python manage.py migrate
   ```
2. **Start the local development server**:
   ```bash
   python manage.py runserver
   ```

## 4. How to Run with Docker Compose
To orchestrate the app and the PostgreSQL database together effortlessly, use Docker Compose:

1. Ensure [Docker Compose](https://docker.com) is installed.
2. Navigate to the folder containing the `docker-compose.yml` file.
3. Build and launch the containers in detached mode:
   ```bash
   docker compose up -d --build --remove-orphans
   ```

*Note: The containers automatically utilize the orchestration script `django.sh` as their entry point. This script handles database container availability checks, applies pending migrations, and manages mock data generation parameters seamlessly on startup.*

## 5. How to Run Database Migrations
When using **Docker Compose**, you do not need to run migrations manually. The `django.sh` script executes `python manage.py migrate` automatically inside the container as the stack boots up.

Manual migration commands are only required in the following scenarios:

### Running Locally (Without Docker)
If you are running the project directly on your host machine, apply schema changes using:
```bash
python manage.py migrate
```

### Developing & Generating New Migrations (Docker)
If you modify the Django models inside the codebase and need to generate or force-apply new migration files while the Docker stack is running, execute:
```bash
# Generate new migration files after structural model edits
docker compose exec ticketapi python manage.py makemigrations

# Force run migrations manually if needed
docker compose exec ticketapi python manage.py migrate
```

## 6. How to Create a Superuser & Default Credentials
By default, the setup system configures a default administrator account:
* **Username:** `admin`
* **Password:** `admin`

*⚠️ **CRITICAL SECURITY NOTE:** It is strongly recommended to update this default password immediately upon your first successful dashboard login.*

If you need to generate an additional custom admin account, use the following instructions:

### Using Docker Compose
Run the command against the **`ticketapi`** service container:
```bash
docker compose exec ticketapi python manage.py createsuperuser
```

### Running Locally
```bash
python manage.py createsuperuser
```
After creation, log in at [http://localhost:8000/admin/](http://localhost:8000/admin/).

## 7. How to Run Tests
A suite of automated tests is available in `ticketapi/tests.py` to verify API logic and structural changes.

### Using Docker Compose
Run the command against the **`ticketapi`** service container:
```bash
docker compose exec ticketapi python manage.py test
```

### Running Locally
```bash
python manage.py test
```
*Note: Always update or expand the `ticketapi/tests.py` file when adding new endpoints or altering data structures.*

## 8. How the CI Pipeline Works
The project utilizes a GitHub Actions workflow defined inside the `.github/workflows/` directory. 
* **Trigger:** Executes automatically on every code push or pull request to the main repository tracking branches.
* **Process:** It provisions a clean virtual environment container runner, installs dependencies from `requirements.txt`, sets up a temporary mock environment/database configuration, and executes the suite using `python manage.py test`.
* **Goal:** Ensures no breaking changes or regressions are merged into the codebase.

## 9. How the CD Process Works
Once the Continuous Integration (CI) pipeline passes successfully:
* **Target:** The code is automatically deployed to a live Cloud Oracle instance.
* **Mechanism:** The workflow safely connects via SSH to the remote instance, pulls the latest codebase updates from your repository, triggers the `django.sh` management orchestration tasks, and uses Docker Compose to rebuild and restart the containers seamlessly without downtime.

## 10. Main Endpoints List
You can view the interactive, auto-generated documentation at:
* **Swagger UI:** [http://localhost:8000/api/schema/swagger-ui](http://localhost:8000/api/schema/swagger-ui)
* **ReDoc:** [http://localhost:8000/api/schema/redoc](http://localhost:8000/api/schema/redoc)

### Summary of Core Routes:
* `POST /api/token/` - Obtain authentication tokens.
* `GET/POST /api/tickets/` - List or create tickets.
* `GET/PUT/DELETE /api/tickets/<id>/` - View, update, or remove a specific ticket.
* `POST /api/tickets/<id>/interactions/` - Post communication messages inside a ticket.
* `GET/POST /api/categories/` - Manage ticket categories (Attendants only).

## 11. Request Examples

### Authenticating a User
`POST /api/token/`
```json
{
  "username": "customer_user",
  "password": "securepassword123"
}
```
**Response:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsIn...",
  "refresh": "eyJhbGciOiJIUzI1NiIsIn..."
}
```

### Creating a Ticket (Customer)
`POST /api/tickets/`  
*Header required: `Authorization: Bearer <access_token>`*
```json
{
  "title": "Cannot access the cloud dashboard",
  "description": "Getting a 403 Forbidden error whenever I click the portal button.",
  "category": 2
}
```
**Response:**
```json
{
  "id": 105,
  "title": "Cannot access the cloud dashboard",
  "status": "Open",
  "created_at": "2026-06-22T11:20:00Z",
  "responsible": null
}
```

---

## Environment Variables Configuration

The full list of environment variables needed to successfully deploy or run the application:

```ini
# Ticket API Configurations
PG_USER=postgres                           # Database user (Must match \$POSTGRES_USER)
PG_PASSWORD=postgres                       # Database password (Must match \$POSTGRES_PASSWORD)
PG_DB=postgres                             # Database name (Must match \$POSTGRES_DB)
PG_HOST=db                                 # Server IP address ('db' if managed by Compose, 'localhost' for local setup)
PG_PORT=5432                               # PostgreSQL database port
SECRET_KEY='django-hash-key'               # Secret key for the Django application
DEBUG=False                                # Django debug status
MOCK_DATA=true                             # Populate database with mock users/tickets via django.sh

# Django Security
ALLOWED_HOSTS="['localhost', '127.0.0.1', 'yourhost.com']"

# PostgreSQL Container Variables
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
```