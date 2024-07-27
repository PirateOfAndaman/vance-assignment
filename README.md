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
	To setup the inital DB 
	```bash
	python3 manage.py migrate
   
6. **Run the development server:**

   ```bash
   python3 manage.py runserver
 