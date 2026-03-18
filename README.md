# Overview
Run the project with
```bash
pip install -r requirements.txt
py migrations.py # Create database tables
uvicorn inventory_management_system.main:app
```

It is worth noting that migrations.py will only create tables if they don't exist, so you will need to delete the db to make changes (or use something like alembic which I haven't got around to doing)

As always, GFG is a massive help: https://www.geeksforgeeks.org/python/fastapi-tutorial/ 

So is the FastAPI documentation:
https://fastapi.tiangolo.com/tutorial/

# Key files
**db.py**- Manages database connections
**main.py**- Runs the server
**migrations.py**- Creates database tables based on models.py
**models.py**- Defines db models
**req.sh**- See below
**schemas**- Defines input/output validation objects

# Req.sh
A simple manual testing script that makes a valid GET, POST, PUT, or DELETE request to /api/Items/

The http verb is not cap-sensitive so "gEt" would also work:

```bash
# Sends a POST request to /api/items/ with expected body values
./req.sh post

# Sends a GET request to /api/items/ with expected body values
./req.sh get
```
Basically, feel free to delete this if you can use postman or another preffered method

