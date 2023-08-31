from setuptools import setup, find_packages
import os

setup(
    name='league-push-ups-backend',
    version=f'0.0.{os.environ.get("BUILD_ID", 1)}',
    packages=find_packages(include=["league_push_ups_backend"]),
    install_requires=[
        "requests",
        "redis",
        "Werkzeug==2.1.2",
        "flask>=2",
        "flask-session",
        "Flask-RESTful",
        "flask-cors",
        "python-ldap",
        "pymysql",
        "peewee",
        "attrs",
        "cattrs",
    ],
    extras_require={
        "test": [
            "mockito",
            "pytest",
            "pylint",
            "mypy",
            "types-requests",
            "types-Flask-Cors",
        ]
    }
)
