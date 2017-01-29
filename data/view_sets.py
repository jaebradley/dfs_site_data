# Create your views here.

from datetime import datetime
from django.db.models import Q
import pytz
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from data.models import DailyFantasySportsSite, Sport, League, Team, Position, LeaguePosition, Season, Player, \
    Game, DailyFantasySportsSiteLeaguePosition, DailyFantasySportsSiteLeaguePositionGroup, \
    DailyFantasySportsSitePlayerGame
from data.serializers import DailyFantasySportsSiteSerializer, SportSerializer, LeagueSerializer, TeamSerializer, PositionSerializer, \
    LeaguePositionSerializer, SeasonSerializer, PlayerSerializer, GameSerializer, \
    DailyFantasySportsSiteLeaguePositionSerializer, \
    DailyFantasySportsSiteLeaguePositionGroupSerializer, DailyFantasySportsSitePlayerGameSerializer


class QuerySetReadOnlyViewSet(ReadOnlyModelViewSet):
    def build_response(self, queryset):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class DfsSiteViewSet(ReadOnlyModelViewSet):
    serializer_class = DailyFantasySportsSiteSerializer

    def get_queryset(self):
        queryset = DailyFantasySportsSite.objects.all().order_by('name')
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)

        return queryset


class SportViewSet(QuerySetReadOnlyViewSet):
    serializer_class = SportSerializer
    queryset = Sport.objects.all().order_by('name')

    def list_sports(self, request, *args, **kwargs):
        return self.build_response(queryset=self.queryset)

    def retrieve_sport(self, request, *args, **kwargs):
        result = self.queryset.filter(id=kwargs.get('sport_id'))
        return self.build_response(queryset=result)


class LeagueViewSet(QuerySetReadOnlyViewSet):
    serializer_class = LeagueSerializer
    queryset = League.objects.all().order_by('name')

    def list_sport_leagues(self, request, *args, **kwargs):
        result = self.queryset.filter(sport__id=kwargs.get('sport_id'))
        return self.build_response(queryset=result)

    def retrieve_sport_leagues(self, request, *args, **kwargs):
        result = self.queryset.filter(sport__id=kwargs.get('sport_id'),
                                      id=kwargs.get('league_id'))

        return self.build_response(queryset=result)


class LeaguePositionViewSet(ReadOnlyModelViewSet):
    serializer_class = LeaguePositionSerializer
    queryset = LeaguePosition.objects.all().order_by('position')

    def get_queryset(self):
        queryset = LeaguePosition.objects.all().order_by('position')
        position = self.request.query_params.get('position', None)
        sport = self.request.query_params.get('sport', None)

        if position is not None:
            queryset = queryset.filter(position__name=position)

        if sport is not None:
            queryset = queryset.filter(league__sport__name=sport)

        return queryset

    def list(self, request, *args, **kwargs):
        result = self.queryset.filter(league__id=kwargs.get('league_id'))

        page = self.paginate_queryset(result)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(result, many=True)

        return Response(serializer.data)

    def detail(self, request, *args, **kwargs):
        result = self.queryset.filter(league__id=kwargs.get('league_id'),
                                      position__id=kwargs.get('position_id'))

        page = self.paginate_queryset(result)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(result, many=True)

        return Response(serializer.data)


class TeamViewSet(QuerySetReadOnlyViewSet):
    serializer_class = TeamSerializer
    queryset = Team.objects.all().order_by('name')

    def list_teams(self, request, *args, **kwargs):
        result = self.queryset.filter(league__sport__id=kwargs.get('sport_id'),
                                      league__id=kwargs.get('league_id'))
        return self.build_response(queryset=result)

    def retrieve_team(self, request, *args, **kwargs):
        result = self.queryset.filter(league__sport__id=kwargs.get('sport_id'),
                                      league__id=kwargs.get('league_id'),
                                      id=kwargs.get('team_id'))
        return self.build_response(queryset=result)


class SeasonViewSet(QuerySetReadOnlyViewSet):
    serializer_class = SeasonSerializer
    queryset = Season.objects.all().order_by('start_time', 'end_time')

    def list_seasons(self, request, *args, **kwargs):
        result = self.queryset.filter(season__league__sport__id=kwargs.get('sport_id'),
                                      season__league__id=kwargs.get('league_id'))

        return self.build_response(queryset=result)


class PlayerViewSet(QuerySetReadOnlyViewSet):
    serializer_class = PlayerSerializer
    queryset = Player.objects.all().order_by('name', 'team__league__name', 'team__name')

    def list_players(self, request, *args, **kwargs):
        result = self.queryset.filter(team__league__sport__id=kwargs.get('sport_id'),
                                      team__league__id=kwargs.get('league_id'))
        return self.build_response(queryset=result)

    def retrieve_player(self, request, *args, **kwargs):
        result = self.queryset.filter(team__league__sport__id=kwargs.get('sport_id'),
                                      team__league__id=kwargs.get('league_id'),
                                      id=kwargs.get('player_id'))

        return self.build_response(queryset=result)


class GameViewSet(QuerySetReadOnlyViewSet):
    serializer_class = GameSerializer
    queryset = Game.objects.all().order_by('start_time')

    def list_games(self, request, *args, **kwargs):
        home_team_results = self.queryset.filter(home_team__league__sport__id=kwargs.get('sport_id'),
                                                 home_team__league__id=kwargs.get('league_id'),
                                                 season__league__id=kwargs.get('league_id'))
        away_team_results = self.queryset.filter(away_team__league__sport__id=kwargs.get('sport_id'),
                                                 away_team__league__id=kwargs.get('league_id'),
                                                 season__league__id=kwargs.get('league_id'))

        combined = home_team_results | away_team_results
        combined = combined.order_by('start_time')
        return self.build_response(queryset=combined)

    def retrieve_game(self, request, *args, **kwargs):
        result = self.queryset.filter(id=kwargs.get('game_id'))

        return self.build_response(queryset=result)


class DailyFantasySportsSiteLeaguePositionViewSet(ReadOnlyModelViewSet):
    serializer_class = DailyFantasySportsSiteLeaguePositionSerializer
    queryset = DailyFantasySportsSiteLeaguePosition.objects.all().order_by('daily_fantasy_sports_site__name',
                                                                           'league_position__league__name',
                                                                           'league_position__position__name')

    def list(self, request, *args, **kwargs):
        result = self.get_queryset().filter(daily_fantasy_sports_site_id=kwargs.get('daily_fantasy_sports_site_id'),
                                            league_position__league_id=kwargs.get('league_id'))
        page = self.paginate_queryset(result)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(result, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        result = self.get_queryset().filter(daily_fantasy_sports_site_id=kwargs.get('daily_fantasy_sports_site_id'),
                                            league_position__league_id=kwargs.get('league_id'),
                                            league_position__position_id=kwargs.get('position_id'))
        page = self.paginate_queryset(result)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(result, many=True)
        return Response(serializer.data)


class DailyFantasySportsSiteLeaguePositionGroupViewSet(QuerySetReadOnlyViewSet):
    serializer_class = DailyFantasySportsSiteLeaguePositionGroupSerializer
    queryset = DailyFantasySportsSiteLeaguePositionGroup.objects.all().order_by(
            'daily_fantasy_sports_site_league_position__daily_fantasy_sports_site__name',
            'daily_fantasy_sports_site_league_position__league_position__league__name',
            'daily_fantasy_sports_site_league_position__league_position__position__name')

    def list_position_groups(self, request, *args, **kwargs):
        result = self.queryset.filter(daily_fantasy_sports_site_league_position__daily_fantasy_sports_site__id=kwargs.get('daily_fantasy_sports_site_id'),
                                      daily_fantasy_sports_site_league_position__league__id=kwargs.get('league_id'))

        return self.build_response(queryset=result)

    def retrieve_position_group(self, request, *args, **kwargs):
        result = self.queryset.filter(daily_fantasy_sports_site_league_position__daily_fantasy_sports_site__id=kwargs.get('daily_fantasy_sports_site_id'),
                                      daily_fantasy_sports_site_league_position__league__id=kwargs.get('league_id'),
                                      id=kwargs.get('position_group_id'))

        return self.build_response(queryset=result)


class DailyFantasySportsSitePlayerGameViewSet(QuerySetReadOnlyViewSet):
    serializer_class = DailyFantasySportsSitePlayerGameSerializer
    queryset = DailyFantasySportsSitePlayerGame.objects.all().order_by('daily_fantasy_sports_site__name',
                                                                       'player__name', 'game__start_time', 'salary')

    def filter_queryset(self, queryset):

        start_time = self.request.query_params.get('start_time', None)
        max_salary = self.request.query_params.get('max_salary', None)
        min_salary = self.request.query_params.get('min_salary', None)

        if start_time is not None:
            queryset = queryset.filter(game__start_time=datetime.fromtimestamp(float(start_time), pytz.utc))

        if max_salary is not None:
            queryset = queryset.filter(salary__lte=float(max_salary))

        if min_salary is not None:
            queryset = queryset.filter(salary__gte=float(min_salary))

        return queryset

    def list_player_games(self, request, *args, **kwargs):
        result = self.queryset.filter(daily_fantasy_sports_site__id=kwargs.get('daily_fantasy_sports_site_id'),
                                      player__team__league__id=kwargs.get('league_id'),
                                      game__home_team__league_id=kwargs.get('league_id'),
                                      game__away_team__league_id=kwargs.get('league_id'),
                                      season__league__id=kwargs.get('league_id'))

        return self.build_response(queryset=result)
