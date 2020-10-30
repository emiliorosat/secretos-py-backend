from peewee import SqliteDatabase,Model,BooleanField, CharField,ForeignKeyField, UUIDField, FloatField, DateField
import models

db = SqliteDatabase("Data/app.db")

## Database Models

class BaseModel(Model):
    class Meta:
        database = db

class User (BaseModel):
    Id = UUIDField(primary_key=True)
    Email = CharField()
    UserName = CharField()
    FullName = CharField()
    Password = CharField()
    Disabled = BooleanField()

class Secret (BaseModel):
    Id = UUIDField(primary_key=True)
    UserId = ForeignKeyField(User)
    Titulo = CharField()
    Description = CharField()
    Value = FloatField()
    Date = DateField()
    Place = CharField()
    Lat = FloatField()
    Lng = FloatField()

class TokenDisabled(BaseModel):
    Token = CharField()
    Date = DateField()


db.connect()
db.create_tables([User, Secret, TokenDisabled])
