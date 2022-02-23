import os

s = "-" * 24
path = os.getcwd().split("\n")
print(path[-1] + " starting...\n")
print(s + " > django makemigrations " + 2 * s)
os.system("python manage.py makemigrations")
print(s + " > django migrate -------" + 2 * s)
os.system("python manage.py migrate")
print(s + " > django runserver -----" + 2 * s)
os.system("python manage.py runserver 9999")

# ID = 9564525
# HASH = 395505c7e277a2be108aa21bb53194e9
# PHONE = +59894940466