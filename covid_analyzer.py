import sys
import requests
import json
import pandas as pd
from datetime import datetime, date
import argparse

class CovidDataAnalyzer:
    """
    A class to analyze COVID-19 data from the Italian Civil Protection Department.
    This class retrieves, processes, and reports data for Italian provinces.
    """

    def __init__(self):
        self.base_url = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/refs/heads/master/dati-json/dpc-covid19-ita-province.json"
        self.regions_data = None
        self.date_start = None
        self.date_end = None

    def fetch_data(self):
        """
        Retrieves COVID-19 data for a specific date or the current day.

        Returns:
            bool: True if data retrieval was successful, False otherwise.
        """
        try:

            # Retrieve all data
            response = requests.get(self.base_url)

            # Check if the response was successful
            if response.status_code == 200:
                all_data = response.json()

                # Convert the list of dictionaries to a DataFrame
                df = pd.DataFrame(all_data)

                self.process_data(df)
                return True
            else:
                print(f"Error: Unable to retrieve data. Status code: {response.status_code}")
                return False

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return False
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON data: {e}")
            return False

    def process_data(self, df):
        """
        Processes COVID-19 data by aggregating cases per region.

        Args:
            data (list): List of data entries from the JSON file.
        """
        # Filter out rows without region information
        df = df[df['denominazione_regione'].notna()]

        # Ensure 'totale_casi' is numeric
        df['totale_casi'] = pd.to_numeric(df['totale_casi'], errors='coerce').fillna(0)

        # Convert date column to datetime
        df['data'] = pd.to_datetime(df['data']).dt.date

        if self.date_start:
            df = df[df['data'] >= self.date_start]

        if self.date_end:
            df = df[df['data'] <= self.date_end]

        # Group by region and sum cases
        region_totals = df.groupby('denominazione_regione')['totale_casi'].sum().reset_index()

        # Sort by cases (descending) and then by region name (ascending)
        region_totals = region_totals.sort_values(
            by=['totale_casi', 'denominazione_regione'],
            ascending=[False, True]
        )

        # Convert to a list of tuples (region, cases) to match original output
        self.regions_data = list(region_totals.itertuples(index=False, name=None))

    def print_report(self):
        """
        Print a report of COVID-19 cases by region to the console.
        """
        if not self.regions_data:
            if self.date_start == self.date_end:
                print(f"No data available (Data for {self.date_start}).")
            else:
                print(f"No data available (Data for {self.date_start} -> {self.date_end}).")
            return

        print(f"\nCOVID-19 Cases by Region (Data for {self.date_start})\n")
        print("Region -> Total Cases")
        print("-" * 44)

        for region, cases in self.regions_data:
            print(f"{region} -> {int(cases)}")

        # Calculate and print total
        total_cases = sum(cases for _, cases in self.regions_data)
        print("-" * 44)
        print(f"{'Total'} -> {int(total_cases)}")

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Analyze COVID-19 data for Italian regions')
    parser.add_argument('--date_start', type=str, help='Date in YYYY-MM-DD format')
    parser.add_argument('--date_end', type=str, help='Date in YYYY-MM-DD format')

    # Parse arguments
    args = parser.parse_args()
    
    # Create the analyzer
    analyzer = CovidDataAnalyzer()

    if args.date_start:
        try:
            analyzer.date_start = datetime.strptime(args.date_start, '%Y-%m-%d').date()
        except ValueError:
            print("Error: The date_start format is incorrect. It must be YYYY-MM-DD")
            sys.exit(1)

    if args.date_end:
        try:
            analyzer.date_end = datetime.strptime(args.date_end, '%Y-%m-%d').date()
        except ValueError:
            print("Error: The date_end format is incorrect. It must be YYYY-MM-DD")
            sys.exit(1)

    # if date_start and date_end is not passed, then it's put today in date_start and date_end
    if not args.date_start or not args.date_end:
        analyzer.date_end = date.today()
        analyzer.date_start = date.today()

    if analyzer.date_start > analyzer.date_end:
        print("Error: The date_start is greater than date_end. The end date must be after the start date.")
        sys.exit(1)

    # Load data
    success = analyzer.fetch_data()

    if not success:
        return

    # Print the report
    analyzer.print_report()

if __name__ == "__main__":
    main()
