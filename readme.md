git init
git clone
python -m venv venv -to create virtual env
pip list
python venv\Scripts\activate.bat-to activate the virtual env
pip install -r requirements.txt
python manage.py makemigrations-whenever new models is created or  updated  we use makemigrations
python manage.py migrate-Adding the tables in database
