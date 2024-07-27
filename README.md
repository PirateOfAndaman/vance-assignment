# Raptor

Backend for Together


### Prerequisites

Ensure you have the following installed on your machine:

- Python 3.10+
- Django

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/PirateOfAndaman/vance-assignment.git
   cd vance-assignment

2. **Create a virtual environment and activate it:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate

3. **Install the dependencies:**

   ```bash
   pip install -r requirements/req.txt
   
4. **Initial Migrations**
	```bash
	python3 manage.py migrate

5. **To populate the inital DB**
    ```bash
    python3 manage.py shell
    from apps.scrapper.service import populate_db
    populate_db()

6. **Start Celery**
    Open a new terminal and enter
    ```bash
    celery -A finance worker --loglevel=info

7. **Setup Celery Beat**
    ```bash
    python manage.py shell
    from django_celery_beat.models import PeriodicTask
    PeriodicTask.objects.update(last_run_at=None)

8. **Start Celery Beat**
    Open a terminal
    ```bash
    celery -A finance beat --loglevel=info


6. **Scrape Historical Data**
    Go to any browser or postman and hit the endpoint
    ```bash
    http://localhost:8000/api/trigger-scrapper

    This will create start an async task to fetch all the historical exchange data, could take 30-45 min to finish

6. **Run the development server:**

   ```bash
   python3 manage.py runserver
 