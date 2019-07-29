import math
import csv
import sqlite3
#Updae these values before taking a reading
connection=sqlite3.connect('camera_cord.db')


c=connection.cursor()



c.execute('CREATE TABLE IF NOT EXISTS camera_cord(camid INT NOT NULL ,cam_x DOUBLE(5, 10), cam_y DOUBLE(5, 10));')


xsensor=36
ysensor=24
focallen=55
altitude=6
xgimbal=70
ygimbal=70

FOV_w=2*(math.degrees(math.atan(xsensor/(2*focallen))))
print(FOV_w)
FOV_h=2*math.degrees((math.atan(ysensor/(2*focallen))))
print(FOV_h)
d_bottom=altitude*(math.tan(math.radians(xgimbal-((1/2)*FOV_w))))
print('bottom: ',d_bottom)
d_top=altitude*(math.tan(math.radians(xgimbal+((1/2)*FOV_w))))
print('top: ', d_top)
d_left=altitude*(math.tan(math.radians(ygimbal-((1/2)*FOV_h))))
print('d_left: ', d_left)
d_right=altitude*(math.tan(math.radians(ygimbal+((1/2)*FOV_h))))
print('d_right: ', d_right)
height_of_footprint=d_right-d_left
width_of_footprint=d_top-d_bottom

print('height_of_footprint: {}, width_of_footprint: {}'.format(height_of_footprint, width_of_footprint))


#TO CALCULTAE THE COORDINATES OF THE FOOTPRINT
sql="SELECT cam_x, cam_y FROM camera_cord;"
c.execute(sql)
result=c.fetchone()
# print(cam_x, type(cam_x[0]))
camera_x=result[0]
camera_y=result[1]
ang_d_bottom=xgimbal-0.5*FOV_w
ang_d_top=xgimbal+0.5*FOV_w
ang_d_left=ygimbal-0.5*FOV_h
ang_d_right=ygimbal+0.5*FOV_h


#This is for demonstration purposes

def change_coordinate():
    sql_new="UPDATE camera_cord SET cam_x={} WHERE camid=1".format(camera_x+1.000)
    c.execute(sql_new)
#NOW x METERS OF DISTANCE BETWEEN DRONE AND FOOTPRINT CAN BE CALCULTED WITH THIS FORMULA x/(111*e3) UNITS OF GEOGRAPHICAL COORDINATES

def make_coordinates(x_percent, y_percent):
     x_cord=x_percent*width_of_footprint
     y_cord=y_percent*height_of_footprint

     longitude1=camera_x+(d_bottom/(111*1000))
     longitude2=camera_x+(d_top/(111*1000))

     latitude1=camera_y+(d_left/(111*1000))
     latitude2=camera_y+(d_right/(111*1000))

     latitude_x=latitude1+(x_cord/(111*1000))
     longitude_y=longitude1+(y_cord/(111*1000))

     return latitude_x, longitude_y

def frame_coordinate():
    longitude1=camera_x+(d_bottom/(111*1000))
    longitude2=camera_x+(d_top/(111*1000))

    latitude1=camera_y+(d_left/(111*1000))
    latitude2=camera_y+(d_right/(111*1000))

    return latitude1, longitude1, latitude2, longitude2
