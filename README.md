# COVID-19 Data Analyzer for Italian Regions

This project provides a tool to analyze COVID-19 data for Italian regions. The tool fetches data from the Italian Civil Protection Department, processes it, and provides options to export it to an Excel file or serve the data via a web API.

## Features

- Fetch COVID-19 data from the Italian Civil Protection Department.
- Process and aggregate cases by region.
- Print a summary report of the total cases by region.
- Export data to an Excel file.
- Provide a web API to serve the data in JSON format.
- Filter data based on a date range.

## Requirements

- Python 3.10 or higher
- Required Python libraries: `requests`, `pandas`, `flask`, `flask_limiter`

You can install the necessary dependencies with the following:

```bash
pip install -r requirements.txt
```

## Usage

## Command Line

You can use the tool from the command line with different options:

1. **Fetching and analyzing data for a specific date range**  
   Use the following command to fetch and analyze data for a specified date range:

   ```bash
   python covid_analyzer.py --date_start YYYY-MM-DD --date_end YYYY-MM-DD
Replace YYYY-MM-DD with the desired start and end date.

Available Options

- --date_start and --date_end: Specify the start and end dates in the format YYYY-MM-DD. If not provided, the tool defaults to today's date.
- --excel: Export the processed data to an Excel file.
- --excel-output: Specify the output file path for the Excel file.
- --server: Start a Flask server to expose the data through an API.
- --file: Provide the path to a local JSON file containing COVID-19 data.

Example Usage

1. Analyze and print COVID-19 data for a specific date range:
    ```bash 
   python covid_analyzer.py --date_start 2021-01-01 --date_end 2021-01-10
   ```
2. Export COVID-19 data to an Excel file:
   ```bash 
   python covid_analyzer.py --excel --excel-output covid_data_2021.xlsx 
   ```
3. Start the Flask web server:
   ```bash 
   python covid_analyzer.py --server
   ```
4. Load data from a local file:
   ```bash 
   python covid_analyzer.py --file /path/to/covid_data.json
   ```

## API

### `GET /covid-data`

Fetches the COVID-19 data for the specified date range. You can pass `date_start` and `date_end` as query parameters in `YYYY-MM-DD` format.

**Example request:**

```
GET /covid-data?date_start=2021-01-01&date_end=2021-01-10
```

**Example response:**

```json
{
  "regions": [
    {"region": "Lombardia", "total_cases": 539147},
    {"region": "Veneto", "total_cases": 312695},
    ...
  ]
}
```
