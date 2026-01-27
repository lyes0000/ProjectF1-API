from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "Fetch all F1 seasons from 2022-2024"

    # Season data: year -> number of rounds
    SEASONS = {
        2022: 22,
        2023: 22,
        2024: 24,
    }

    def add_arguments(self, parser):
        parser.add_argument(
            '--delay',
            type=int,
            default=5,
            help='Seconds to wait between requests (default: 5)'
        )
        parser.add_argument(
            '--start-year',
            type=int,
            default=2022,
            help='First year to fetch (default: 2022)'
        )
        parser.add_argument(
            '--end-year',
            type=int,
            default=2024,
            help='Last year to fetch (default: 2024)'
        )

    def handle(self, *args, **options):
        delay = options['delay']
        start_year = options['start_year']
        end_year = options['end_year']
        
        # Filter seasons based on year range
        seasons_to_fetch = {
            year: rounds 
            for year, rounds in self.SEASONS.items() 
            if start_year <= year <= end_year
        }
        
        if not seasons_to_fetch:
            self.stdout.write(self.style.ERROR(
                f"No seasons found between {start_year} and {end_year}"
            ))
            return
        
        total_rounds = sum(seasons_to_fetch.values())
        
        self.stdout.write(self.style.WARNING(
            f"\n{'='*70}"
        ))
        self.stdout.write(self.style.WARNING(
            f"Fetching F1 Data: {start_year}-{end_year}"
        ))
        self.stdout.write(self.style.WARNING(
            f"Total seasons: {len(seasons_to_fetch)}"
        ))
        self.stdout.write(self.style.WARNING(
            f"Total rounds: {total_rounds}"
        ))
        self.stdout.write(self.style.WARNING(
            f"Estimated time: {total_rounds * 0.2:.2f} minutes"
        ))
        self.stdout.write(self.style.WARNING(
            f"{'='*70}\n"
        ))
        
        completed_years = 0
        completed_rounds = 0
        
        for year, rounds in seasons_to_fetch.items():
            self.stdout.write(f"\n{'='*70}")
            self.stdout.write(f"Starting {year} season ({rounds} rounds)")
            self.stdout.write(f"{'='*70}\n")
            
            try:
                call_command(
                    'fetch_season',
                    year=year,
                    end_round=rounds,
                    delay=delay
                )
                completed_years += 1
                completed_rounds += rounds
                self.stdout.write(self.style.SUCCESS(
                    f"\n✓ {year} season complete!\n"
                ))
                
            except KeyboardInterrupt:
                self.stdout.write(self.style.WARNING(
                    "\n\nStopped by user (Ctrl+C)"
                ))
                break
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"\n✗ {year} season failed: {str(e)}\n"
                ))
                
                try:
                    response = input("Continue to next year? (y/n): ")
                    if response.lower() != 'y':
                        break
                except KeyboardInterrupt:
                    self.stdout.write(self.style.WARNING(
                        "\nStopped by user"
                    ))
                    break
        
        # Final summary
        self.stdout.write(f"\n{'='*70}")
        self.stdout.write(self.style.SUCCESS("FINAL SUMMARY"))
        self.stdout.write(f"{'='*70}")
        self.stdout.write(f"Years completed: {completed_years}/{len(seasons_to_fetch)}")
        self.stdout.write(f"Rounds completed: {completed_rounds}/{total_rounds}")
        self.stdout.write(f"{'='*70}\n")