import os
import django

# Initialize Django environment when api package is imported
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
if not os.environ.get("DJANGO_SETTINGS_LOADED"):
    django.setup()
    os.environ["DJANGO_SETTINGS_LOADED"] = "1"
