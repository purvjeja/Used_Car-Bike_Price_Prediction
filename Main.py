import pandas as pd
import numpy as np
car_data=pd.read_csv('Data\Cars\CAR_6000.csv')
car_data1=pd.read_csv('Data\Cars\CAR_4000.csv')
car_data1.append(car_data)
print(car_data)
