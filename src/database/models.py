from peewee import (
    CharField,
    IntegerField,
    ForeignKeyField,
    Model,
    SqliteDatabase,
    ManyToManyField,
)


DB_PATH = "torneio-suico.db"


class BaseModel(Model):
    class Meta:
        database = SqliteDatabase(DB_PATH, pragmas={"foreign_keys": 1})


class Contestant(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField(unique=True)


class Tournament(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField(unique=True)
    current_round = IntegerField(default=1)
    rounds = IntegerField(default=1)
    contestants = ManyToManyField(Contestant, backref="tournaments")


class Match(BaseModel):
    id = IntegerField(primary_key=True)
    contestant1 = ForeignKeyField(Contestant, backref="matches_as_contestant1")
    contestant2 = ForeignKeyField(Contestant, backref="matches_as_contestant2")
    winner = ForeignKeyField(Contestant, backref="matches_as_winner", null=True)
    round = IntegerField()
    contestant1_score = IntegerField(null=True)
    contestant2_score = IntegerField(null=True)
    tournament = ForeignKeyField(Tournament, backref="matches")


class Round(BaseModel):
    id = IntegerField(primary_key=True)
    number = IntegerField()
    tournament = ForeignKeyField(Tournament, backref="rounds")
    matches = ManyToManyField(Match, backref="rounds")
    contestants = ManyToManyField(Contestant, backref="rounds")
    winners = ManyToManyField(Contestant, backref="rounds_won")
    losers = ManyToManyField(Contestant, backref="rounds_lost")
