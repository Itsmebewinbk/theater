from fabric import task
@task
def deploy(c):
    c.run("pip freeze > requirements.txt") 
    c.run("python manage.py runserver")
    c.run("celery -A THeaTRe_BooKiNG_aPP beat  -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler")
    c.run ("celery -A THeaTRe_BooKiNG_aPP worker -l info")
   