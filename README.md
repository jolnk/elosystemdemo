          hello. this might help.

git clone https://github.com/jolnk/elosystem.git .

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt 

cd elo_system

python manage.py makemigrations 

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver
