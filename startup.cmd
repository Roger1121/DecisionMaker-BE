docker-compose up -d
pip install -r requirements.txt
python manage.py makemigrations mcda
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata ./mcda/seed/problem.json
python manage.py loaddata ./mcda/seed/criterion.json
python manage.py loaddata ./mcda/seed/option.json
python manage.py loaddata ./mcda/seed/criterion-option.json
python manage.py runserver