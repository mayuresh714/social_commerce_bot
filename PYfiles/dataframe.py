import pandas as pd
from __init__ import *

file_path =  cwd+"/newcsv.csv"
df= pd.read_csv(r"{}".format(file_path))
df['image'] = cwd + "/files/IMAGE"
df = df.set_index("sr")

print(df['image'].iloc[0])

 
 
