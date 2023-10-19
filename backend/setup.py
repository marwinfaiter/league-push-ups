from setuptools import setup, find_packages

VERSION = "0.0.0"

setup(
    name='league-push-ups-backend',
    version=VERSION,
    packages=find_packages(include=["league_push_ups_backend", "league_push_ups_backend.*"]),
    install_requires=[
        "requests",
        "redis",
        "Werkzeug==2.1.2",
        "flask>=2",
        "flask-login",
        "flask-socketio",
        "flask-session",
        "Flask-RESTful",
        "flask-cors",
        "python-ldap",
        "pymysql",
        "peewee",
        "peewee-db-evolve",
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
            "types-peewee",
            "types-setuptools",
        ]
    }
)
