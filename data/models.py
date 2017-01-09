from __future__ import unicode_literals

# Create your models here.


from django.db.models import Model, BigIntegerField, IntegerField, CharField, DateTimeField, ForeignKey, CASCADE


class DfsSite(Model):
    name = CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name


class Sport(Model):
    name = CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name


class Position(Model):
    sport = ForeignKey(Sport, on_delete=CASCADE, related_name='position_sport')
    name = CharField(max_length=100)

    class Meta:
        unique_together = ('sport', 'name')

    def __unicode__(self):
        return '{0} - {1}'.format(self.sport, self.name)


class DfsPosition(Model):
    site = ForeignKey(DfsSite, on_delete=CASCADE)
    position = ForeignKey(Position, on_delete=CASCADE)
    dfs_site_position_id = IntegerField()

    class Meta:
        unique_together = ('site', 'position')

    def __unicode__(self):
        return '{0} - {1}'.format(self.site, self.position)


class League(Model):
    sport = ForeignKey(Sport, on_delete=CASCADE)
    name = CharField(max_length=100)

    class Meta:
        unique_together = ('sport', 'name')

    def __unicode__(self):
        return '{0} - {1}'.format(self.sport, self.name)


class Team(Model):
    league = ForeignKey(League, on_delete=CASCADE)
    name = CharField(max_length=100)

    class Meta:
        unique_together = ('league', 'name')

    def __unicode__(self):
        return '{0} - {1}'.format(self.league, self.name)


class Season(Model):
    league = ForeignKey(League, on_delete=CASCADE)
    start_time = DateTimeField()
    end_time = DateTimeField()

    class Meta:
        unique_together = ('league', 'start_time', 'end_time')

    def __unicode__(self):
        return '{0} - {1} - {2}'.format(self.league, self.start_time, self.end_time)


class TeamSeason(Model):
    team = ForeignKey(Team, on_delete=CASCADE)
    season = ForeignKey(Season, on_delete=CASCADE)

    class Meta:
        unique_together = ('team', 'season')

    def __unicode__(self):
        return '{0} - {1}'.format(self.team, self.season)


class Player(Model):
    team_season = ForeignKey(TeamSeason, on_delete=CASCADE)
    name = CharField(max_length=250)
    identifier = BigIntegerField()

    class Meta:
        unique_together = ('team_season', 'name', 'identifier')

    def __unicode__(self):
        return '{0} - {1} - {2}'.format(self.team_season, self.name, self.identifier)


class DfsPlayer(Model):
    player = ForeignKey(Player, on_delete=CASCADE)
    site = ForeignKey(DfsSite, on_delete=CASCADE)
    site_identifier = BigIntegerField()

    class Meta:
        unique_together = ('player', 'site')

    def __unicode__(self):
        return '{0} - {1} - {2}'.format(self.player, self.site, self.site_identifier)


class PlayerPosition(Model):
    player = ForeignKey(Player, on_delete=CASCADE)
    position = ForeignKey(Position, on_delete=CASCADE)

    class Meta:
        unique_together = ('player', 'position')

    def __unicode__(self):
        return '{0} - {1}'.format(self.player, self.position)


class Game(Model):
    home_team = ForeignKey(Team, on_delete=CASCADE, related_name='home_team')
    away_team = ForeignKey(Team, on_delete=CASCADE, related_name='away_team')
    start_time = DateTimeField()

    class Meta:
        unique_together = ('home_team', 'away_team', 'start_time')

    def __unicode__(self):
        return '{0} - {1} - {2}'.format(self.home_team, self.away_team, self.start_time)


class PlayerGame(Model):
    player = ForeignKey(Player, on_delete=CASCADE)
    game = ForeignKey(Game, on_delete=CASCADE)

    class Meta:
        unique_together = ('player', 'game')

    def __unicode__(self):
        return '{0} - {1}'.format(self.player, self.game)