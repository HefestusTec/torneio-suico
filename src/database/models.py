from peewee import (
    CharField,
    IntegerField,
    ForeignKeyField,
    Model,
    SqliteDatabase,
    ManyToManyField,
)


DB_PATH = "persist/torneio-suico.db"


class BaseModel(Model):
    class Meta:
        database = SqliteDatabase(DB_PATH, pragmas={"foreign_keys": 1})


class Contestant(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()


class Tournament(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField(unique=True)
    setup_stage = IntegerField(default=0)
    current_round = IntegerField(default=1)
    rounds = IntegerField(default=1)
    max_round_score = IntegerField(default=1)
    contestants = ManyToManyField(Contestant, backref="tournaments")


class Match(BaseModel):
    id = IntegerField(primary_key=True)
    tournament = ForeignKeyField(Tournament, backref="matches")
    round = IntegerField()
    contestant1 = ForeignKeyField(Contestant, backref="matches_as_contestant1")
    contestant2 = ForeignKeyField(
        Contestant, backref="matches_as_contestant2", null=True
    )
    contestant1_score = IntegerField(default=0)
    contestant2_score = IntegerField(default=0)
