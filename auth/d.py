
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
conn = sqlite3.connect('loc.db')
c = conn.cursor()
c1=0
c2=0
c3=0
c4=0
affected_c1=0
affected_c2=0
affected_c3=0
affected_c4=0
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




    
