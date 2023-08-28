from setuptools import setup, find_packages
import os

setup(
    name='league-push-ups-backend',
    version=f'0.0.{os.environ.get("BUILD_ID", 1)}',
    packages=find_packages(include=["league_push_ups_backend"]),
    install_requires=[
        "requests",
        "flask",
        "flask_restful",
        "flask_cors",
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
