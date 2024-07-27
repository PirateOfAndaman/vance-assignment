# Vance Assignment

Backend for Asssignment


### Prerequisites

Ensure you have the following installed on your machine:

- Python 3.10+
- Redis

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
   
4. **Apply Initial Migrations**
	```bash
	python3 manage.py migrate

5. **To populate the inital DB**
    ```bash
    python3 manage.py shell
    from apps.scrapper.service import populate_db
    populate_db()

6. **Start your local redis instance**
    ```bash
    redis-server

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

6. **Run the development server:**

   ```bash
   python3 manage.py runserver
 

6. **Scrape Historical Data**
    Go to any browser or postman and hit the endpoint
    ```bash
    http://localhost:8000/api/trigger-scrapper

    This will create start an async task to fetch all the historical exchange data, could take 30-45 min to finish


### API DOCUMENTATION
### Task 1
## api/forex-data
    
    http://localhost:8000/api/forex-data?from=USD&to=INR&period=1W

    This endpoint takes in a few query parameters as follows:

    from: This will be the from currency code (e.g., GBP, AED).

    to: This will be the to currency code (e.g., INR).

    period: This will be the timeframe for which you want to query data (e.g., 1M, 3M - 1M indicates you are querying exchange data from the last one month).

    Entering wrong info, will get a response about how to send correct parameters
## api/trigger-scrapper
    This endpoint is meant for initial populating of all the historical exchange rates over the last 10000 days
### Task2
## Cron Setup
    The cron job is setup such that, it will fetch the data of GBP-INR and AED-INR every week and add it to the table