#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys



def folder_creation():
    if not os.path.isdir("./static"):
        os.makedirs("./static")
    
    if not os.path.isdir("./static/turf_images"):
        os.makedirs("./static/turf_images")

def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "turfbooking.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    folder_creation()
    main()
