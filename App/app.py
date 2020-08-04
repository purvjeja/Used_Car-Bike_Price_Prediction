from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def Home():
    return render_template('index.html')


@app.route('/CAR', methods=['GET'])
def CAR():
    return render_template('CAR.html')

@app.route('/BIKE', methods=['GET'])
def BIKE():
    return render_template('BIKE.html')

@app.route('/CAR_Result', methods=['GET','POST'])
def car():
 if request.method == 'POST':  
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
    
    X_train1, X_test1, Y_train1, Y_test1=train_test_split(Full_Car_Data[['year','kilometers_Driven','new_fuel','new_transmission','new_owner','mileage']],Full_Car_Data[['selling_price']],test_size=0.2,random_state=3)
    linearRegression = LinearRegression()
    linearRegression.fit(X_train1,Y_train1)
    car_predicted=linearRegression.predict(X_test1)
    from sklearn.ensemble import RandomForestRegressor
    rf = RandomForestRegressor(n_estimators = 100)
    rf.fit(X_train1, Y_train1.values.ravel())
    y_pred = rf.predict(X_test1)
    score=r2_score(Y_test1,y_pred)
    year = int(request.form["year"])
    km = int(request.form["km"])
    fuel = int(request.form["fuel"])
    trans = int(request.form["trans"])
    owner = int(request.form["times_sold"])
    mileage = int(request.form["mileage"])
    user_car_prediction=linearRegression.predict([[year,km,fuel,trans,owner,mileage]])
    res = float(str(user_car_prediction)[2:-2])
    output=round(res,2)
    score=round(score,2)
    score=score*100
    
    if output<1:
            return render_template('result_car_negative.html')
    else:
            global car
            global count
            count=0
            car="Oops! We Are Unable To Suggest You Best Car For Your Input :("
            def findcarname(columns):
                    global car
                    global count
                    name=columns[0]
                    year_used=columns[1]
                    price=columns[2]
                    transmission=columns[3]
                    price1=price+100000
                    price2=price-100000
                    if year_used==year:
                        if transmission==trans:
                            if (output <= price1 and output >= price2):
                              car=name
                              count+=1
            Full_Car_Data[['name','year','selling_price','new_transmission']].apply(findcarname,axis=1)

            if count==0:
                    return render_template('result_car.html',text="{}".format(output),predicted_score="{}".format(score),car_suggestion="{}".format(car))
            else:
                    return render_template('result_car.html',text="{}".format(output),predicted_score="{}".format(score),car_suggestion="\"{}\" Model Fits Best To Your Inputed Data :)".format(car))
 else:
    return render_template('CAR.html')
        

@app.route('/BIKE_Result', methods=['GET','POST'])
def bike():
 if request.method == 'POST':
    bike_data=pd.read_csv('Data\BIKE\BIKE_1000.csv')

    bike_data.loc[bike_data['owner'] == '1st owner', 'new_owner'] = 0                      # 0 for 1st owner
    bike_data.loc[bike_data['owner'] == '2nd owner', 'new_owner'] = 1                      # 1 for 2st owner
    bike_data.loc[bike_data['owner'] == '3rd owner', 'new_owner'] = 2                      # 3 for 3st owner   
    bike_data.loc[bike_data['owner'] == '4th owner', 'new_owner'] = 3                      # 4 for 4st owner
       
    X_train2, X_test2, Y_train2, Y_test2=train_test_split(bike_data[['year','km_driven','new_owner']],bike_data[['selling_price']],test_size=0.10,random_state=0)
    linearRegre= LinearRegression()
    linearRegre.fit(X_train2,Y_train2)
    #bike_predicted=linearRegre.predict(X_test2)
    bike_names=bike_data['name']
    year = int(request.form["y"])
    owner = int(request.form["sold"])
    km = int(request.form["km"])
    #print(linearRegre.score(X_test2,Y_test2))
    #print(bike_predicted)
    user_bike_predicted=linearRegre.predict([[year,km,owner]])
    res = float(str(user_bike_predicted)[2:-2])
    output=round(res,2)
    output=round(output)
    from sklearn.ensemble import RandomForestRegressor
    rf = RandomForestRegressor(n_estimators = 100)
    rf.fit(X_train2, Y_train2.values.ravel())
    y_pred2 = rf.predict(X_test2)
    score=r2_score(Y_test2,y_pred2)
    score=round(score,2)
    score=score*100
    if output<1:
        return render_template('result_bike_negative.html')
    else:
        global bike
        bike="Oops! We Are Unable To Suggest You Best Bike For Your Input :("
        global count
        count=0
        def findbikename(columns):
            global bike
            global count
            name=columns[0]
            this_year=columns[1]
            price=columns[2]
            price1=price+10000
            price2=price-10000
            if this_year==year:
                    if (output <= price1 and output >= price2):
                             bike=name
                             count+=1
        bike_data[['name','year','selling_price']].apply(findbikename,axis=1)

        if count==0:
            return render_template('result_bike.html',text="{}".format(output),predicted_score="{}%".format(score),bike_suggestion="{}".format(bike))
        else:
            return render_template('result_bike.html',text="{}".format(output),predicted_score="{}%".format(score),bike_count_suggestion="Total Number Of Bikes Which Relates Your Inputed Data Is  {} , ".format(count),bike_suggestion="Out Of Which \"{}\" Is Best For You :)".format(bike))
 else:
    return render_template('BIKE.html')

if __name__=="__main__":
    app.run(debug=True)
