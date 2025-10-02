# Flight Data Integration Project

Combine airport, population, income, airline delay, and NOAA weather data into a master dataset for analysis.

---

## Features
- Merges airport & runway info with population and income data  
- Incorporates airline delay causes  
- Aggregates NOAA 2024 weather data (precipitation)  

---

## Requirements
- Python 3.8+  
- pandas  
- numpy  

Install dependencies:

```bash
pip install pandas numpy
```
Project_Data/
├─ APT_BASE.csv
├─ APT_RWY.csv
├─ Population_City.csv
├─ Population_State.csv
├─ Household_Income_City.csv
├─ Household_Income_State.csv
├─ Airline_Delay_Cause.csv
├─ NOAA_2024.csv   # Downloaded from NOAA, see instructions below
main.py
processed/
└─ master_dataset.csv   # Output file
## Datasets

### Local CSVs
- `APT_BASE.csv`, `APT_RWY.csv` – Airport info  
- `Population_City.csv`, `Population_State.csv` – Population data  
- `Household_Income_City.csv`, `Household_Income_State.csv` – Income data  
- `Airline_Delay_Cause.csv` – Delay data  

### NOAA 2024 Weather Data
The NOAA Global Historical Climatology Network (GHCN) daily data is too large for GitHub. To obtain it:

1. Go to [NOAA GHCN daily data by year](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/by_year/)  
2. Download the file `2024.csv.gz`  
3. Extract it to obtain `NOAA_2024.csv`  
4. Place `NOAA_2024.csv` in the `Project_Data/` folder  

> **Tip:** Make sure the file name matches exactly (`NOAA_2024.csv`) or update the path in `main.py`.  

---

## How to Run

1. Ensure all datasets are in the `Project_Data/` folder.  
2. Run the main script:

```bash
python main.py
```
