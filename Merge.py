import pandas as pd
import os

# -------------------------------
# Load datasets (Replace with your specific paths)
# -------------------------------
apt_base = pd.read_csv(r"C:\Users\jrbru\Project_Data\APT_BASE.csv", low_memory=False)
apt_rwy = pd.read_csv(r"C:\Users\jrbru\Project_Data\APT_RWY.csv", low_memory=False)
household_income_city = pd.read_csv(r"C:\Users\jrbru\Project_Data\Household_Income_City.csv", low_memory=False)
household_income_state = pd.read_csv(r"C:\Users\jrbru\Project_Data\Household_Income_State.csv", low_memory=False)
population_city = pd.read_csv(r"C:\Users\jrbru\Project_Data\Population_City.csv", low_memory=False)
population_state = pd.read_csv(r"C:\Users\jrbru\Project_Data\Population_State.csv", low_memory=False)
noaa = pd.read_csv(r"C:\Users\jrbru\Project_Data\NOAA_2024.csv", low_memory=False)
airline_delay = pd.read_csv(r"C:\Users\jrbru\Project_Data\Airline_Delay_Cause.csv", low_memory=False)

# -------------------------------
# Process Runway Data
# -------------------------------
apt_rwy_agg = apt_rwy.groupby('ARPT_ID').agg({
    'RWY_LEN': 'max',
    'SURFACE_TYPE_CODE': 'first',
    'RWY_LGT_CODE': 'first'
}).reset_index()

# -------------------------------
# Merge airport base with runway info
# -------------------------------
airports = pd.merge(
    apt_base[['ARPT_ID', 'ARPT_NAME', 'CITY', 'STATE_CODE', 'LAT_DECIMAL', 'LONG_DECIMAL']],
    apt_rwy_agg,
    on='ARPT_ID',
    how='left'
)

# -------------------------------
# Normalize city names for merging
# -------------------------------
def normalize_city(city_name):
    if pd.isna(city_name):
        return city_name
    city = city_name.lower()
    city = city.split('(')[0]
    city = city.replace(',', '')
    city = city.strip()
    return city

airports['CITY_NORM'] = airports['CITY'].apply(normalize_city)

# -------------------------------
# Merge City Population
# -------------------------------
population_city = population_city.rename(columns={'NAME': 'CITY', 'B01003_001E': 'Population'})
population_city['CITY_NORM'] = population_city['CITY'].apply(normalize_city)

airports = pd.merge(
    airports,
    population_city[['CITY_NORM', 'Population']],
    on='CITY_NORM',
    how='left'
)

# -------------------------------
# Merge State Population for fallback
# -------------------------------
# Map state abbreviations to full names
state_abbrev_to_name = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
    'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'DC': 'District of Columbia',
    'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois',
    'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana',
    'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan',
    'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana',
    'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
    'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota',
    'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania',
    'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee',
    'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington',
    'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming', 'PR': 'Puerto Rico'
}

airports['STATE_FULL'] = airports['STATE_CODE'].map(state_abbrev_to_name)

# Merge State Population
population_state = population_state.rename(columns={'NAME': 'STATE', 'B01003_001E': 'State_Population'})
airports = pd.merge(
    airports,
    population_state[['STATE', 'State_Population']],
    left_on='STATE_FULL',
    right_on='STATE',
    how='left'
)
airports.drop(columns=['STATE'], inplace=True)

# Fill missing city-level population with state-level
airports['Population'] = airports['Population'].fillna(airports['State_Population'])
airports.drop(columns=['State_Population'], inplace=True)

# -------------------------------
# Merge City Median Income
# -------------------------------
household_income_city = household_income_city.rename(columns={'NAME': 'CITY', 'B19013_001E': 'Median_Income'})
household_income_city['CITY_NORM'] = household_income_city['CITY'].apply(normalize_city)

airports = pd.merge(
    airports,
    household_income_city[['CITY_NORM', 'Median_Income']],
    on='CITY_NORM',
    how='left'
)

# Merge State Median Income
household_income_state = household_income_state.rename(columns={'NAME': 'STATE', 'B19013_001E': 'State_Median_Income'})
airports = pd.merge(
    airports,
    household_income_state[['STATE', 'State_Median_Income']],
    left_on='STATE_FULL',
    right_on='STATE',
    how='left'
)
airports.drop(columns=['STATE'], inplace=True)

# Fill missing city-level income with state-level
airports['Median_Income'] = airports['Median_Income'].fillna(airports['State_Median_Income'])
airports.drop(columns=['State_Median_Income', 'STATE_FULL'], inplace=True)

# -------------------------------
# Clean and Aggregate NOAA Data
# -------------------------------
noaa = noaa.rename(columns={'ASN00040223': 'STATION', '20240101': 'DATE', 'PRCP': 'PRCP'})
noaa['PRCP'] = pd.to_numeric(noaa['PRCP'], errors='coerce')
noaa = noaa.dropna(subset=['PRCP'])
noaa_agg = noaa.groupby('STATION').agg({'PRCP': 'mean'}).reset_index()

# -------------------------------
# Merge Airline Delay data
# -------------------------------
master = pd.merge(
    airline_delay,
    airports,
    left_on='airport',
    right_on='ARPT_ID',
    how='left'
)

# -------------------------------
# Save master dataset
# -------------------------------
output_dir = os.path.join(os.getcwd(), "processed")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "master_dataset.csv")

master.to_csv(output_path, index=False)
print(f"Master dataset saved to {output_path}")
