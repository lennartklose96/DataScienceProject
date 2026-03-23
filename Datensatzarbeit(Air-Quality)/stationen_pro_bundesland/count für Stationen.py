import pandas as pd

df = pd.read_csv(r"C:\Users\Anwender\arxiv_tutorial\arxiv_tutorial\DS\Datensatzarbeit(Air-Quality)\4.1 urban_ländlich_präziser_PM10\vorstädtisch_Industrie_IDs.csv")

erste_spalte = df.iloc[:, 0].sort_values().tolist()
print(erste_spalte)

# you can use this to get the station_ids from the csv files if they are listed there
# they also get sorted by size to get a better visualization