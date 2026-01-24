"""
This file allows us to resolve Drivers that are participating (active) 
in a specific year (season) as our db contains all drivers according to fetched years, 
it also helps find drivers active for futur races not in our db, so we don't predict for inactive (retired) drivers
"""

from django.utils import timezone
from datetime import datetime
from races.models import Race
from drivers.models import Driver

import os
import fastf1

# safe cache path
CACHE_DIR = "/tmp/f1_cache"
os.makedirs(CACHE_DIR, exist_ok=True)
fastf1.Cache.enable_cache(CACHE_DIR)


def resolve_active_race_driver(year, race_name):
    """
    Drivers active in a season.
    Can adjust it later
    """
    # 1st case: Race is already stored in our DB:
    try:
        race = Race.objects.get(year=year, name=race_name)
        return list(
            Driver.objects.filter(raceresult__race=race).distinct()
        )
    except Race.DoesNotExist:
        pass

    # 2nd case : Race is not in DB but exist in FastF1 (COMPLETED RACE)
    try:
        session = fastf1.get_session(year, race_name, "R")
        session.load()

        return Driver.objects.filter(code__in=session.results["Abbreviation"]
        )
    except Exception:
        pass
    # Fallback: if race is not in FastF1, we fetch latest race in FastF1:
    try:
        schedule = fastf1.get_event_schedule(year)
        past_events = schedule[schedule["EventDate"] < datetime.now()]
        last_event = past_events.iloc[-1]

        session = fastf1.get_session(year, last_event["EventName"], "R")
        session.load()

        return Driver.objects.filter(
            code__in=session.results["Abbreviation"]
        )
    except Exception:
        pass

    # Final fallback: Season drivers from DB
    drivers = Driver.objects.filter(
        raceresult__race__year=year
    ).distinct()

    if not drivers.exists():
        raise ValueError("No drivers available for prediction")
    
    return list(drivers)