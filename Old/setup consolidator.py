import pandas as pd
import os






class consolidate:
    def consolidate():


        path = "C:/Screener/tmp/subsetups/"

        dir_list = os.listdir(path)


        try:
            setups = pd.read_feather(r"C:\Screener\tmp\setups.feather")
        except:
            setups = pd.DataFrame()


        for f in dir_list:
            df = pd.read_feather(path + f)
            setups = pd.concat([setups,df])

        setups.reset_index(inplace = True,drop = True)
        setups.to_feather(r"C:\Screener\tmp\setups.feather")






if __name__ = '__main__':
    consolidate.consolidate()









