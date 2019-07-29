import folium
import os
import json

# Create map object

# Edit this b variable like i've done in this dataset
b = [[28.6129,77.2295],[28.6271,77.2166],[28.5245,77.1855]]
name = ['India Gate','Jantar Mantar','Qutub Minar']
map = folium.Map(location = b[0], zoom_start = 4)
feature_group = folium.FeatureGroup("Locations")

for i in range(len(b)):
    feature_group.add_child(folium.Marker(location=b[i],popup =name[i]))

map.add_child(feature_group)

map.save('templates/map.html')
