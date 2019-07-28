import folium
import os
import json

# Create map object

a = input()
b = input()
m = folium.Map(location=[a,b], zoom_start=8)
print(a)
print(b)
# Global tooltip
tooltip = 'Click For More Info'

# Create custom marker icon
logoIcon = folium.features.CustomIcon('logo.png', icon_size=(50, 50))

# Vega data
vis = os.path.join('data', 'vis.json')

# Geojson Data
overlay = os.path.join('data', 'overlay.json')

# Create markers
folium.Marker([a,b],
              popup='<strong>Location One</strong>',
              tooltip=tooltip).add_to(m),
folium.Marker([a,b],
              popup='<strong>Location Two</strong>',
              tooltip=tooltip,
              icon=folium.Icon(icon='cloud')).add_to(m),
folium.Marker([a,b],
              popup='<strong>Location Three</strong>',
              tooltip=tooltip,
              icon=folium.Icon(color='purple')).add_to(m),
folium.Marker([a,b],
              popup='<strong>Location Four</strong>',
              tooltip=tooltip,
              icon=folium.Icon(color='green', icon='leaf')).add_to(m),
folium.Marker([a,b],
              popup='<strong>Location Five</strong>',
              tooltip=tooltip,
              icon=logoIcon).add_to(m),
folium.Marker([a,b],
              popup=folium.Popup(max_width=450).add_child(folium.Vega(json.load(open(vis)), width=450, height=250))).add_to(m)

# Circle marker
folium.CircleMarker(
    location=[a,b],
    radius=50,
    popup='My Birthplace',
    color='#428bca',
    fill=True,
    fill_color='#428bca'
).add_to(m)

# Geojson overlay
folium.GeoJson(overlay, name='cambridge').add_to(m)

# Generate map
m.save('map.html')
