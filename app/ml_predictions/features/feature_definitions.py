"""
Defines all features used for ML predictions
Each feature is a function that calculates a value for a driver in a specific race
"""

import pandas as pd
from django.db.models import Avg, Count, Sum
from races.models import RaceResult


class FeatureDefinitions:
    """
    All feature calculation method
    """

    @staticmethod
    def grid_position(driver_id, race):
        """
        Starting grid position (from Qualifying)
        This is often the most important feature!!
        """
        try:
            result = RaceResult.objects.get(race_id=race, driver_id=driver_id)
            #for now our RaceResult model do not contain grid_position
            #so for now, we'll use postion as placeholder
            return result.position # TODO: Add actual grid position
        except RaceResult.DoesNotExist:
            return 20 #Default to last position, note: from 2026 there will be 22 drivers.
        
    @staticmethod
    def driver_points_season(driver_id, race):
        """
        Driver's total points in the season before this race
        """
        from races.models import Race

        season_races = Race.objects.filter(year=race.year, round__lt=race.round)
        points = RaceResult.objects.filter(
            driver_id=driver_id,
            race__in=season_races
        ).aggregate(total=Sum('points'))['total']
        return points or 0
    
    @staticmethod
    def driver_avg_position_last_5(driver_id, race):
        """
        Driver's average finishing position in the last 5 races
        """
        from races.models import Race

        # Get races before this one
        previous_races = Race.objects.filter(
            year__lt=race.year
        ) | Race.objects.filter(
            year=race.year,
            round__lt=race.round
        )
        previous_races = previous_races.order_by('-year', '-round')[:5]


        avg_pos = RaceResult.objects.filter(
            driver_id=driver_id,
            race__in=previous_races
        ).aggregate(avg=Avg('position'))['avg']

        return avg_pos if avg_pos else 1.0 # Default middle position
    
    @staticmethod
    def driver_wins_season(driver_id, race):
        """
        Number of wins this season before this race
        """
        from races.models import Race

        season_races = Race.objects.filter(year=race.year, round__lt=race.round)
        wins = RaceResult.objects.filter(
            driver_id=driver_id,
            race__in=season_races,
            position=1
        ).count()
        return wins
    
    @staticmethod
    def team_avg_points_last_5(driver_id, race):
        """
        Average points for driver's team in last 5 races
        """
        from races.models import Race
        from drivers.models import Driver

        driver = Driver.objects.get(id=driver_id)
        if not driver.team:
            return 0
        
        previous_races = Race.objects.filter(
            year__lt=race.year
        ) | Race.objects.filter(
            year=race.year,
            round__lt=race.round
        )
        previous_races = previous_races.order_by('-year', '-round')[:5]

        # get all drivers fomr same team
        team_drivers = Driver.objects.filter(team=driver.team)

        avg_points = RaceResult.objects.filter(
            driver__in=team_drivers,
            race__in=previous_races
        ).aggregate(avg=Avg('points'))['avg']

        return avg_points if avg_points else 0
    
    @staticmethod
    def dnf_rate(driver_id, race):
        """
        Driver's DNF rate this season before this race
        Assumes DNF = position IS NULL or position = 0
        """
        from races.models import Race

        season_races = Race.objects.filter(
            year=race.year,
            round__lt=race.round
        )

        results = RaceResult.objects.filter(
            driver_id=driver_id,
            race__in=season_races
        )

        total = results.count()
        if total == 0:
            return 0.0

        dnfs = results.filter(
            dnf=True
        ).count() + results.filter(
            position=0
        ).count()

        return dnfs / total

    
    @staticmethod
    def driver_podiums_season(driver_id, race):
        from races.models import Race

        season_races = Race.objects.filter(year=race.year, round__lt=race.round)
        podiums = RaceResult.objects.filter(
            driver_id=driver_id,
            race__in=season_races,
            position__lte=3
        ).count()
        return podiums
    
# Define features to use for training
FEATURE_LIST = [
    #'grid_position',
    'driver_avg_position_last_5',
    'driver_points_season',
    'driver_wins_season',
    'driver_podiums_season',
    'team_avg_points_last_5',
    'dnf_rate',
]