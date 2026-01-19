from django.core.management.base import BaseCommand
from django.core.management import call_command
import time


class Command(BaseCommand):
    help = "Fetch entire F1 season data from FastF1"

    def add_arguments(self, parser):
        parser.add_argument(
            '--year',
            type=int,
            required=True,
            help='Season year to fetch'
        )
        parser.add_argument(
            '--start-round',
            type=int,
            default=1,
            help='Starting round number (default: 1)'
        )
        parser.add_argument(
            '--end-round',
            type=int,
            default=24,
            help='Ending round number (default: 24)'
        )
        parser.add_argument(
            '--delay',
            type=int,
            default=5,
            help='Seconds to wait between requests (default: 5)'
        )

    def handle(self, *args, **options):
        year = options['year']
        start_round = options['start_round']
        end_round = options['end_round']
        delay = options['delay']
        
        self.stdout.write(self.style.WARNING(
            f"\nFetching {year} season (rounds {start_round}-{end_round})"
        ))
        self.stdout.write(f"Delay between requests: {delay} seconds\n")
        
        successful = 0
        failed = 0
        skipped = 0
        
        for round_num in range(start_round, end_round + 1):
            self.stdout.write(f"\n{'='*70}")
            self.stdout.write(f"Round {round_num}/{end_round}")
            self.stdout.write(f"{'='*70}")
            
            try:
                # Call the existing fetch_f1_data command
                call_command('fetch_f1_data', year=year, round=round_num)
                successful += 1
                self.stdout.write(self.style.SUCCESS(f"✓ Round {round_num} fetched successfully!"))
                
            except Exception as e:
                error_msg = str(e)
                
                # Check if race already exists
                if 'already exists' in error_msg.lower() or 'already fetched' in error_msg.lower():
                    skipped += 1
                    self.stdout.write(self.style.WARNING(f"⊙ Round {round_num} already in database"))
                else:
                    failed += 1
                    self.stdout.write(self.style.ERROR(f"✗ Round {round_num} failed: {error_msg}"))