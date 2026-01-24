from django.core.management.base import BaseCommand
from app.races.services.single_race_fetch_service import RaceFetchService

class Command(BaseCommand):
    help = "Fetch Formula 1 race data using FastF1"

    def add_arguments(self, parser):
        parser.add_argument('--year', type=int, help='Season year')
        parser.add_argument('--round', type=int, help='Round number')
        parser.add_argument('--race_name', type=str, help='Race name')

    def handle(self, *args, **options):
        year = options['year']
        round = options.get('round')
        race_name = options.get('name_name')

        if not round and not race_name:
            self.stdout.write(
                self.style.ERROR('Error: Either --round or --race must be provided')
            )
            return
        
        identifier = race_name if race_name else f"Round {round}"
        self.stdout.write(f"Fetching F1 data for {year} - {identifier}")

        try:
            service = RaceFetchService()
            race, created = service.fetch_race_data(
                year=year, 
                race_name=race_name,
                round=round
            )

            status = "created" if created else "updated"
            self.stdout.write(self.style.SUCCESS(f"Race {status}: {race}"))
        except ValueError as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Unexpected error: {str(e)}"))