# HIMS App

## Description
This is a FastAPI-based demo application.
This project can also run directly with Python without needing Docker.

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
