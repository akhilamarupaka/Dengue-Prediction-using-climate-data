from flask import Blueprint, render_template,session 
from flask_login import login_required, current_user,login_user
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle,requests
import geocoder
from datetime import datetime
import sqlite3
from math import radians, cos, sin, asin, sqrt
c1=0
c2=0
c3=0
c4=0
affected_c1=0
affected_c2=0
affected_c3=0
affected_c4=0
g = geocoder.ip('me')
lat1=g.latlng[0]
lon1=g.latlng[1]
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle,requests
main= Blueprint('main', __name__)
model = pickle.load(open('model.pkl', 'rb'))
@main.route('/profile')
@login_required
def profile():
    conn = sqlite3.connect('loc.db')
    c = conn.cursor()
    email=session['email']
    d1={'a40':'Above 40','b40':'Below 40','i40':'Intermittent'}
    d2={0:"Unlikely",1:"Likely"}
    c.execute("select name,lat,lon,fever,checked_symptoms,date_time,type from user_prof5 where email=(?)",(email,))
    user=[]
    for row in c.fetchall():
        l=[]
        l.append(row[5])
        l.append(row[0])
        l.append(d1[row[3]])
        y=row[4]
        y=y.replace('[','')
        y=y.replace(']','')
        y=y.replace('\'','')
        l.append(y)
        l.append(d2[row[6]])
        user.append(l)
    user=user[::-1]
    conn.commit()
    conn.close()
    return render_template('profile.html', name=current_user.name, len = len(user),user=user)

@main.route('/')
@login_required
def index():
    return render_template('index.html')
@main.route('/home')
@login_required
def home():
        conn = sqlite3.connect('loc.db')
        c = conn.cursor()
        global c1,c2,c3,c4,affected_c1,affected_c2,affected_c3,affected_c4
        c1=0
        c2=0
        c3=0
        c4=0
        affected_c1=0
        affected_c2=0
        affected_c3=0
        affected_c4=0
        global lat1,lon1
        c.execute("select * from loc")
        for row in c.fetchall():
                lat2=row[0]
                lon2=row[1]
                ans=dist(lat1, lat2, lon1, lon2)
                print(ans, "  ",row[2])
                if(ans<=0.5):
                        c1=c1+1
                if(ans<=0.5) and row[2]==1:
                        affected_c1+=1
                if ans<=1:
                        c2=c2+1
                if ans<=1 and row[2]==1:
                        affected_c2+=1
                if ans<=5 :
                        c3=c3+1
                if ans<=5 and row[2]==1:
                        affected_c3+=1
                if ans<=10 :
                        c4=c4+1
                if ans<=10 and row[2]==1:
                        affected_c4+=1
        print("Within 0.5 km Out of ",c1," , ",affected_c1 ,"are effected")
        print("Within 1 km Out of ",c2," , ",affected_c2 ,"are effected")
        print("Within 5 km Out of ",c3," , ",affected_c3 ,"are effected")
        print("Within 10 km Out of ",c4," , ",affected_c4 ,"are effected")
        conn.commit()
        conn.close()
        
        return render_template('card.html',variable1=c1,variable2=affected_c1,variable3=c2,variable4=affected_c2,variable5=c3,variable6=affected_c3,variable7=c4,variable8=affected_c4)
@main.route('/check',methods=['POST'])
@login_required
def check():
    if request.method == 'POST':
        email=session['email']
        global lat1,lon1
        x="https://www.google.com/maps/embed?pb=!1m16!1m12!1m3!1d15227.614150536452!2d78.48651673098736!3d17.416416316055994!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!2m1!1sdoctors%20near%20me!5e0!3m2!1sen!2sin!4v1613972334657!5m2!1sen!2sin" 
        type=1
        date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        option1 = request.form['rmatch']
        option2=request.form.getlist('match')
        option3=request.form['r1match']
        dengue_fever=[ "high fever","headaches","Pain behind the eyes", "Severe joint and muscle pain","Nausea","Vomiting","Skin rash","No appetite"]
        severe_dengue=["Swollen glands","Severe abdominal pain","Bleeding gums","Vomiting blood","Rapid breathing","Fatigue"]
        final=""
        match_1=list(set(option2).intersection(dengue_fever))
        match_2=list(set(option2).intersection(severe_dengue))
        if(option1=='a40'):
            if(len(match_1)<2 ):
                type=0
                final="Minimal/No symptoms of Dengue fever"
            elif(len(match_2)<2):
                type=0
                final="Minimal/No symptoms of Severe Dengue fever"
        if(option1=='a40' and len(match_1)>=2):
            if(option3=='y'):
                type=1
                final="You may have dengue fever"
            elif(option3=='n'):
                 type=1
                 final="There is a possibility for dengue fever"
        if((option1=='i40' or option1=='a40') and len(match_2)>=2):
            if(option3=='y'):
                type=1
                final="You may have severe dengue fever"
            elif(option3=='n'):
                 type=1
                 final="There is a possibility for severe dengue fever"
        if(option1=='b40'):
            type=0
            final="No symptoms of dengue fever and severe dengue fever"
       
        conn = sqlite3.connect('loc.db')
        c = conn.cursor()
        c.execute("INSERT INTO user_prof5(email,name,lat,lon,fever,checked_symptoms,date_time,type) VALUES(?,?,?,?,?,?,?,?)",(email,current_user.name,lat1,lon1,option1,str(option2),date_time,type))

        conn.commit()
        conn.close()
        
        global c1,c2,c3,c4,affected_c1,affected_c2,affected_c3,affected_c4
        home()
    return render_template('card.html',x=x, prediction_text=final,lat1=lat1,lon1=lon1,type=type,variable1=c1,variable2=affected_c1,variable3=c2,variable4=affected_c2,variable5=c3,variable6=affected_c3,variable7=c4,variable8=affected_c4)
@main.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [float(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = round(prediction[0], 0)

    return render_template('index.html', prediction_text='No of cases should be {}'.format(output))

@main.route('/predict_api',methods=['POST'])
def predict_api():
    #loc_features =[float(x) for x in request.form.values()]
    BASE_URL = "https://api.openweathermap.org/data/2.5/onecall?"
    lat=request.form["lat"]
    lon=request.form["lon"]
    API_KEY = "6f8938a5166c14962cace23bf85d4c1b"
    # upadting the URL
    URL = BASE_URL + "lat="+lat+"&lon="+lon+"&exclude=hourly" + "&appid=" + API_KEY
# HTTP request
    response = requests.get(URL)
    # checking the status code of the request
    if response.status_code == 200:
        data = response.json()
        # getting the main dict block
        main = data['daily']
        # getting temperature
        temperature = main[0]['temp']['day']-273.15
        # getting the humidity
        humidity = main[0]['humidity']
        dew_point = main[0]['dew_point']-273.15
        temperature_min=main[0]['temp']['min']-273.15
        temperature_max=main[0]['temp']['max']-273.15
        temperature_average=(temperature_min+temperature_max)/2
        temperature_diurnal_range=(temperature_max-temperature_min)
        specific_hum=(325/humidity)
        form_final_features = [temperature,temperature_average,dew_point,humidity,specific_hum,temperature_diurnal_range,temperature_max]
        final_features_1= [np.array(form_final_features)]
        prediction = model.predict(final_features_1)
        output_1 = round(prediction[0], 0)
        print(f"Temperature: {temperature}")
        print(f"Dew point: {dew_point}")
        print(f"Temperature max: {temperature_max}")
        print("Temperature average: %0.2f" %temperature_average)
        print("Temperature tdtr range : %0.1f" %temperature_diurnal_range)
        print(f"Humidity: {humidity}")
    else:
        print("Error in the HTTP request")
   
    return render_template('index.html', prediction_text_1='No of cases should be {}'.format(output_1))
  

def dist(lat1, lat2, lon1, lon2): 
	
	# The math module contains a function named 
	# radians which converts from degrees to radians. 
	lon1 = radians(lon1) 
	lon2 = radians(lon2) 
	lat1 = radians(lat1) 
	lat2 = radians(lat2) 
	
	# Haversine formula 
	dlon = lon2 - lon1 
	dlat = lat2 - lat1 
	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2

	c = 2 * asin(sqrt(a)) 
	
	# Radius of earth in kilometers. Use 3956 for miles 
	r = 6371
	
	# calculate the result 
	return(c * r) 




    
    

    


if __name__ == "__main__":
    main.run(debug=True)



