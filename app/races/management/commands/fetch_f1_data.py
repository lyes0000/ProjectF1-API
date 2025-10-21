from django.core.management.base import BaseCommand
import os
import fastf1
from fastf1 import plotting
from races.models import Race, RaceResult
from drivers.models import Driver

class Command(BaseCommand):
    help = "Fetch Formula 1 race data using FastF1"

    def add_arguments(self, parser):
        parser.add_argument('--year', type=int, help='Season year')
        parser.add_argument('--round', type=int, help='Round number')

    def handle(self, *args, **options):
        year = options.get('year', 2024)
        rnd = options.get('round', 1)

        cache_dir = "/tmp/f1_cache"
        mpl_dir = "/tmp/matplotlib"
        os.makedirs(cache_dir, exist_ok=True)
        os.makedirs(mpl_dir, exist_ok=True)
        os.environ['MPLCONFIGDIR'] = mpl_dir
        fastf1.Cache.enable_cache(cache_dir)


        self.stdout.write(f"Fetching F1 data for {year} Round {rnd}")
        session = fastf1.get_session(year, rnd, 'R')
        session.load() # Loads race data

        race, _ = Race.objects.get_or_create(
            name=session.event['EventName'],
            circuit=session.event['Location'],
            year=year,
            round=rnd,
            date=session.event['EventDate']
        )

        for drv in session.drivers:
            info = session.get_driver(drv)
            driver, _ = Driver.objects.get_or_create(
                code=info['Abbreviation'],
                defaults={
                    'first_name': info['FirstName'],
                    'last_name': info['LastName'],
                    'nationality': info.get('CountryCode', ''),
                }
            )
            laps = session.laps.pick_drivers(drv)
            fastest = laps['LapTime'].min().total_seconds() if not laps.empty else None

            RaceResult.objects.update_or_create(
                race=race,
                driver=driver,
                defaults={
                    'position': int(info['Position']) if info.get('Position') else 0,
                    'points': float(info.get('Points', 0)),
                    'fastest_lap_time' : fastest,
                }
            )
        self.stdout.write(self.style.SUCCESS(f"Data loaded for {race}"))