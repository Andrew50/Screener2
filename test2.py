import time
from multiprocessing import Pool, current_process
import pandas as pd
import Scan 



df = pd.read_feather(r"C:\Screener\tmp\ml.feather")

print(df)