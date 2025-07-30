# HIMS App

## Description
This is a FastAPI-based demo application.
This project can also run directly with Python without needing Docker.
This application consists of a login page with basic authentication(user details provided). 
Features : Add inventory, Modify inventory(update/delete), Search inventory with item name/type, View inventory related insights, Receive alert on successful task completion.
Additionally a dark mode view option is also provided.

## Setup Instructions
Existing user : 
  username : admin
  password : P@ssword124
### Prerequisites(
- Docker
- Docker Compose
- To run locally: Python 3.10+
- pip
- (Optional) virtualenv

### Run the application
```bash
docker-compose up --build

OR

git clone https://github.com/abantikaChail/hims-app.git
cd hims-app

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
