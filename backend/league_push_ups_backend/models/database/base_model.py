from peewee import Model, MySQLDatabase
import os

database = MySQLDatabase(
    database=os.environ.get("MYSQL_DATABASE"),
    user=os.environ.get("MYSQL_USER"),
    password=os.environ.get("MYSQL_PASSWORD"),
    host=os.environ.get("MYSQL_HOST"),
    port=os.environ.get("MYSQL_PORT", 3306)
)

class BaseModel(Model):
    class Meta:
        database = database
