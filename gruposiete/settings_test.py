from gruposiete.settings import *

SECRET_KEY = os.environ.get(
    "SECRET_KEY", "django-insecure-3r4y$y04o#(n+1v0+gdpggwiq!v=g$b*0@b(c1_*uxq3t_5eh^"
)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}