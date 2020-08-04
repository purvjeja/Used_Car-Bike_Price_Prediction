from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
car_data = pd.read_csv('BIKE_1000.csv')
#print(car_data)
car_year=2010
main_price=39590
count=0
car=" Oops! We Are Unable To Suggest You Best Bike For Your Input :("
def findcarname(columns):
        global car
        global count
        name=columns[0]
        year=columns[1]
        price=columns[2]
        price1=price+10000
        price2=price-10000
        if year==car_year:
                 if (main_price <= price1 and main_price >= price2):
                         car=name
                         count+=1
car_data[['name','year','selling_price']].apply(findcarname,axis=1)
print(count)
print(car)
