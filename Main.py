import pandas as pd
import numpy as np
import time
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics

car_data = pd.read_csv('Data\Cars\CAR_6000.csv')
Full_Car_Data = pd.read_csv('Data\Cars\CAR_10000.csv')



#Data Cleaning And Modification

car_data['mileage'] = car_data['mileage'].str.rstrip('kmpl')        # Removing the 'kmpl' from the mileage column
car_data['mileage'] = car_data['mileage'].str.rstrip('km/kg')       # Removing the 'km/kg' from the mileage column

    
car_data.loc[car_data['transmission'] == 'Manual', 'new_transmission'] = 0                      # 0 for Manual      
car_data.loc[car_data['transmission'] == 'Automatic', 'new_transmission'] = 1                   # 1 for Automatic   

car_data.loc[car_data['fuel_Type'] == 'CNG', 'new_fuel'] = 0                                    # 0 for CNG
car_data.loc[car_data['fuel_Type'] == 'LPG', 'new_fuel'] = 1                                    # 1 for LPG
car_data.loc[car_data['fuel_Type'] == 'Petrol', 'new_fuel'] = 2                                 # 2 for Petrol
car_data.loc[car_data['fuel_Type'] == 'Diesel', 'new_fuel'] = 3                                 # 3 for Diesel
   


car_data.dropna(inplace = True) #empty Data removing


X=car_data.iloc[:,[1,2,8,9]].values
Y=car_data.iloc[:,6].values

X_train,X_test,Y_train,Y_test= train_test_split(X,Y, test_size=0.10,random_state=0)

regressor=LinearRegression()
regressor.fit(X_train,Y_train)
y_pred=regressor.predict(X_test)
#print(y_prediction)
#print(regressor.score(X_test,Y_test))


def predict_mileage(input_data):
    y_prediction=regressor.predict(input_data)
    if(y_prediction < 10): y_prediction=y_prediction+13.43 
    return  y_prediction


Full_Car_Data['mileage'] = Full_Car_Data['mileage'].str.rstrip('kmpl')        # Removing the 'kmpl' from the mileage column
Full_Car_Data['mileage'] = Full_Car_Data['mileage'].str.rstrip('km/kg')       # Removing the 'km/kg' from the mileage column


Full_Car_Data.loc[Full_Car_Data['transmission'] == 'Manual', 'new_transmission'] = 0                      # 0 for Manual      
Full_Car_Data.loc[Full_Car_Data['transmission'] == 'Automatic', 'new_transmission'] = 1                   # 1 for Automatic   

Full_Car_Data.loc[Full_Car_Data['fuel_Type'] == 'CNG', 'new_fuel'] = 0                                    # 0 for CNG
Full_Car_Data.loc[Full_Car_Data['fuel_Type'] == 'LPG', 'new_fuel'] = 1                                    # 1 for LPG
Full_Car_Data.loc[Full_Car_Data['fuel_Type'] == 'Petrol', 'new_fuel'] = 2                                 # 2 for Petrol
Full_Car_Data.loc[Full_Car_Data['fuel_Type'] == 'Diesel', 'new_fuel'] = 3                                 # 3 for Diesel

Full_Car_Data.loc[Full_Car_Data['owner_Type'] == 'First', 'new_owner'] = 0                                # 0 for First
Full_Car_Data.loc[Full_Car_Data['owner_Type'] == 'First Owner', 'new_owner'] = 0

Full_Car_Data.loc[Full_Car_Data['owner_Type'] == 'Second', 'new_owner'] = 1                               # 1 for Second
Full_Car_Data.loc[Full_Car_Data['owner_Type'] == 'Second Owner', 'new_owner'] = 1
    
Full_Car_Data.loc[Full_Car_Data['owner_Type'] == 'Third', 'new_owner'] = 2                                # 2 for Third
Full_Car_Data.loc[Full_Car_Data['owner_Type'] == 'Third Owner', 'new_owner'] = 2

Full_Car_Data.loc[Full_Car_Data['owner_Type'] == 'Fourth & Above', 'new_owner'] = 3                       # 3 for Fourth
Full_Car_Data.loc[Full_Car_Data['owner_Type'] == 'Fourth & Above Owner', 'new_owner'] = 3                  
Full_Car_Data.loc[Full_Car_Data['owner_Type'] == 'Test Drive Car', 'new_owner'] = 3  

Full_Car_Data.dropna(subset=['new_fuel'],inplace=True)


def mileageempty(columns):
    mileage=columns[0]
    year=columns[1]
    km=columns[2]
    transmission=columns[3]
    fuel=columns[4]
    
    if pd.isnull(mileage):
        data_for_mileage = predict_mileage([[year,km,transmission,fuel]])
        return data_for_mileage
    else:
        return mileage


Full_Car_Data['mileage']=Full_Car_Data[['mileage','year','kilometers_Driven','new_transmission','new_fuel']].apply(mileageempty,axis=1)
#print(Full_Car_Data.count())

X_train1, X_test1, Y_train1, Y_test1=train_test_split(Full_Car_Data[['year','kilometers_Driven','new_fuel','new_transmission','new_owner','mileage']],Full_Car_Data[['selling_price']],test_size=0.01,random_state=3)
linearRegression = LinearRegression()
linearRegression.fit(X_train1,Y_train1)
car_predicted=linearRegression.predict(X_test1)
#users_prediction=linearRegression.predict(X_test1)


#print(linearRegression.score(X_test1,Y_test1))

from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor(n_estimators = 100)
rf.fit(X_train1, Y_train1.values.ravel())
y_pred = rf.predict(X_test1)
from sklearn.metrics import r2_score
#print(r2_score(Y_test1,y_pred))
#users_prediction=linearRegression.predict(X_test1)





#Bike Model

bike_data=pd.read_csv('Data\BIKE\BIKE_1000.csv')

bike_data.loc[bike_data['owner'] == '1st owner', 'new_owner'] = 0                      # 0 for 1st owner
bike_data.loc[bike_data['owner'] == '2nd owner', 'new_owner'] = 1                      # 1 for 2st owner
bike_data.loc[bike_data['owner'] == '3rd owner', 'new_owner'] = 2                      # 3 for 3st owner   
bike_data.loc[bike_data['owner'] == '4th owner', 'new_owner'] = 3                      # 4 for 4st owner

       
X_train2, X_test2, Y_train2, Y_test2=train_test_split(bike_data[['year','new_owner','km_driven']],bike_data[['selling_price']],test_size=0.10,random_state=0)
linearRegre= LinearRegression()
linearRegre.fit(X_train2,Y_train2)
bike_predicted=linearRegre.predict(X_test2)
#print(linearRegre.score(X_test2,Y_test2))
#print(bike_predicted)

from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor(n_estimators = 100)
rf.fit(X_train2, Y_train2.values.ravel())
y = rf.predict(X_test2)
from sklearn.metrics import r2_score
#print(r2_score(Y_test2,y))
#user_bike_predicted()



print("Hello Vaibhav Nai toh Pragya :)")
switch_number=int(input("Want To know the Price of BIKE or CAR? (Press 1 for CAR And 2 for BIKE Then press Enter)  :  "))
if switch_number==1:
     year=int(input('Enter the Model Year of your Vehicle You Want? Ex:- 2010 : '))
     km=int(input('How much Kilometer Runed Vehicle You Want? Ex:- 28000KM : '))
     fuel=int(input('Which Type of Fuel? (press 0 for CNG,1 for LPG.2 for Petrol,3 for Diesel) : '))
     trans=int(input('Manual Or Automatic ? (Press 0 for Manual and 1 for Automatic) : '))
     owner=int(input('How Many time sold vehicle you want?(press 0 for second hand,1 for third hand,2 for fourth hand) : '))
     mileage=int(input('How much mileage you want? Ex :- 20 : '))
     user_car_prediction=linearRegression.predict([[year,km,fuel,trans,owner,mileage]])
     res = str(user_car_prediction)[2:-2]
     print("We Recommend You to keep your Budget this much for your car =>",res)
     print('We Are ',r2_score(Y_test1,y_pred)*100,'% Sure About our Predictions  :)') 
     time.sleep(10)
     
elif switch_number==2:
     year=int(input('Enter the Model Year of your Vehicle You Want? Ex:- 2010 : '))
     km=int(input('How much Kilometer Runed Vehicle You Want? Ex:- 28000KM : '))
     owner=int(input('How Many time sold vehicle you want?(press 0 for second hand,1 for third hand,2 for fourth hand) : '))
     user_bike_predicted=linearRegre.predict([[year,owner,km]])
     res = str(user_bike_predicted)[2:-2]
     print("We Recommend You to keep your Budget this much for Your Bike =>",res)
     print("We Are ",r2_score(Y_test2,y)*100,"% Sure About our Predictions  :)")
     time.sleep(10)
else:
     print("Aree Yaarr sirf 1 ya 2 dabane Bola tha, tum bhi na  :( ")
