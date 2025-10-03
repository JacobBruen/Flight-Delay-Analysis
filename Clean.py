import pandas as pd

# Load master dataset
master = pd.read_csv(r"C:\Users\jrbru\Project_Data\processed\master_dataset.csv")

# Define predictors (5) and targets (3)
predictors = master[['RWY_LEN', 'Population', 'Median_Income', 'SURFACE_TYPE_CODE', 'RWY_LGT_CODE']]
targets = master[['arr_del15', 'arr_cancelled', 'arr_diverted']]

# Example: bin Population into categories
def bin_population(pop):
    if pd.isna(pop): 
        return 'Unknown'
    elif pop < 100000:
        return 'Small'
    elif pop < 1000000:
        return 'Medium'
    else:
        return 'Large'

master['Population_Bin'] = master['Population'].apply(bin_population)

# Example: bin arr_del15 into categories
def bin_delays(x):
    if x < 50:
        return 'Low'
    elif x < 200:
        return 'Medium'
    else:
        return 'High'

master['arr_del15_Bin'] = master['arr_del15'].apply(bin_delays)

# Save cleaned dataset with bins
master.to_csv(r"C:\Users\jrbru\Project_Data\processed\cleaned_master.csv", index=False)
print("Cleaned dataset saved.")
