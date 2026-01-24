import os
import fastf1
import math
import pandas as pd
import numpy as np
from datetime import datetime
from .models import Race, RaceResult
from drivers.models import Driver

class RaceFetchService:
    """Service to handle race data fetching from FastF1"""

    def __init__(self):
        cache_dir = "/tmp/f1_cache"
        mpl_dir = "/tmp/matplotlib"
        os.makedirs(cache_dir, exist_ok=True)
        os.makedirs(mpl_dir, exist_ok=True)
        os.environ['MPLCONFIGDIR'] = mpl_dir
        fastf1.Cache.enable_cache(cache_dir)

    def _clean_float(self, value):
        """Convert NaN/Inf to None for database storage"""
        if value is None:
            return None
        try:
            if math.isnan(value) or math.isinf(value):
                return None
            return float(value)
        except (TypeError, ValueError):
            return None
        
    def _convert_to_date(self, date_value):
        """Convert datetime to date, handling timezone issues"""
        if date_value is None:
            return None
        # If it's already a date, just return it
        if hasattr(date_value, 'date'):
            return date_value.date()
        # If it is a Pandas Timestamp
        if hasattr(date_value, 'to_pydatetime'):
            return date_value.to_pydatetime().date()
        return date_value

    def fetch_race_data(self, year, round=None, race_name=None):
        """
        Fetch and save race data
        Returns: (race, created) tuple
        Raises: ValueError if data fetch fails
        """
        try:

            identifier = race_name if race_name else round
            session = fastf1.get_session(year, identifier, 'R')
            session.load()

            event_date = self._convert_to_date(session.event['EventDate'])

            race, created = Race.objects.get_or_create(
                year=year,
                round=session.event['RoundNumber'],
                defaults={
                    'name': session.event['EventName'],
                    'circuit': session.event['Location'],
                    'country': session.event['Country'],
                    'date': event_date
                }
            )

            if not created:
                race.name = session.event['EventName']
                race.circuit = session.event['Location']
                race.date = event_date
                race.save()

            # Save race results
            for drv in session.drivers:
                info = session.get_driver(drv)
                driver, _ = Driver.objects.get_or_create(
                    code=info['Abbreviation'],
                    defaults={
                        'first_name': info['FirstName'],
                        'last_name': info['LastName'],
                        'number': str(info['DriverNumber']),
                        'nationality': info.get('CountryCode', ''),
                    }
                )

                laps = session.laps.pick_drivers(drv)
                fastest = None
                if not laps.empty and 'LapTime' in laps.columns:
                    try:
                        fastest_lap = laps['LapTime'].min()
                        fastest_sec = self._clean_float(fastest_lap.total_seconds())
                        #fastestlap = session.laps.pick_drivers(drv).pick_fastest
                    except:
                        fastest = None
                
                points = self._clean_float(info.get('Points', 0))
                if points is None:
                    points = 0.0

                RaceResult.objects.update_or_create(
                    race=race,
                    driver=driver,
                    defaults={
                        'position': int(info['Position']) if info.get('Position') else 0,
                        'points': float(info.get('Points', 0)),
                        'fastest_lap_time': fastest_sec,
                        'dnf': bool(info.get('dnf', False))
                    }
                )

            return race, created
        
        except Exception as e:
            raise ValueError(f"Failed to fetch race data: {str(e)}")