Flight Data Integration Project

Combine airport, population, income, airline delay, and NOAA weather data into a master dataset for analysis.

Features

Merges airport & runway info with population and income data

Incorporates airline delay causes

Aggregates NOAA 2024 weather data (precipitation)

Requirements

Python 3.8+

pandas, numpy

Install dependencies:

pip install pandas numpy

Datasets
Local CSVs

APT_BASE.csv, APT_RWY.csv – Airport info

Population_City.csv, Population_State.csv – Population data

Household_Income_City.csv, Household_Income_State.csv – Income data

Airline_Delay_Cause.csv – Delay data

NOAA 2024 Weather Data

Download 2024.csv.gz

Extract to NOAA_2024.csv

Place in Project_Data/

Run
python main.py


Output: processed/master_dataset.csv

Notes

City-level missing data is filled with state-level values.

NOAA precipitation is averaged by station.

Large datasets require sufficient memory.
