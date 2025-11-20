import os
import fastf1
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

            race, created = Race.objects.get_or_create(
                name=session.event['EventName'],
                circuit=session.event['Location'],
                country=session.event['Country'],
                year=year,
                round=session.event['RoundNumber'],
                date=session.event['EventDate']
            )

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
                fastest = laps['LapTime'].min().total_seconds() if not laps.empty else None
                fastestlap = session.laps.pick_drivers(drv).pick_fastest

                RaceResult.objects.update_or_create(
                    race=race,
                    driver=driver,
                    defaults={
                        'position': int(info['Position']) if info.get('Position') else 0,
                        'points': float(info.get('Points', 0)),
                        'fastest_lap_time': fastest,
                    }
                )

            return race, created
        
        except Exception as e:
            raise ValueError(f"Failed to fetch race data: {str(e)}")