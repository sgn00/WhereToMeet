from getDistance import * 
import pandas as pd

mrt  = pd.read_csv('mrt.csv')

def main():
    dic = {1: (1.3868, 103.89), 2: (25.2744, 133.7751), 3: (51.5074, 0.1278)}
    print(getTopKClosest(dic, mrt, 3))

main()