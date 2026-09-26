from dotenv import load_dotenv
import os

# READ THE .ENV FILE
load_dotenv()

my_db_password = os.getenv("DB_PASSWORD")
print(my_db_password)

my_app_password = os.getenv("WEBSERVER_PASSWORD")
print(my_app_password)