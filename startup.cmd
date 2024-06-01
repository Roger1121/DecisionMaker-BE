docker-compose up -d
pip install -r requirements.txt
python manage.py makemigrations mcda
python manage.py makemigrations
python manage.py migrate
python manage.py runserver