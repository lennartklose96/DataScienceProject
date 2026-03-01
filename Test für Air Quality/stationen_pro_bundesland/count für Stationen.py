import pandas as pd

df = pd.read_csv(r"c:\Users\Anwender\arxiv_tutorial\arxiv_tutorial\DS\Test für Air Quality\stationen_pro_bundesland\stationen-UBA.csv")

erste_spalte = df.iloc[:, 0].sort_values().tolist()
print(erste_spalte)