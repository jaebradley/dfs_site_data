from django.core.management.base import BaseCommand

from data.management.commands.insert_dfs_site import Command as DfsSiteInserterCommand
from data.management.commands.insert_sport import Command as SportInserterCommand
from data.management.commands.insert_league import Command as LeagueInserterCommand
from data.management.commands.insert_team import Command as TeamInserterCommand
from data.management.commands.insert_position import Command as PositionInserterCommand
from data.management.commands.insert_league_position import Command as LeaguePositionInserterCommand
from data.management.commands.insert_draft_kings_leagues import Command as DraftKingsInserterCommand
from data.management.commands.insert_season import Command as SeasonInserterCommand
from data.management.commands.insert_team_season import Command as TeamSeasonInserterCommand


class Command(BaseCommand):
    def __init__(self, stdout=None, stderr=None, no_color=False):
        super(Command, self).__init__(stdout, stderr, no_color)

    def handle(self, *args, **options):
        Command.insert()

    @staticmethod
    def insert():
        DfsSiteInserterCommand.insert()
        SportInserterCommand.insert()
        LeagueInserterCommand.insert()
        TeamInserterCommand.insert()
        PositionInserterCommand.insert()
        LeaguePositionInserterCommand.insert()
        DraftKingsInserterCommand.insert()
        SeasonInserterCommand.insert()
        TeamSeasonInserterCommand.insert()
