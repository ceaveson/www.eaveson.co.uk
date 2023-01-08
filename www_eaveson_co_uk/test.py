from dotenv import load_dotenv
import os 

load_dotenv()

DATABASE_URI = os.getenv('DATABASE_URI')
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET')
SECRET_KEY = os.getenv('SECRET_KEY')

print (DATABASE_URI)
print(WEBHOOK_SECRET)
print(SECRET_KEY)