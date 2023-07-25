
import pandas as pd
data = pd.read_csv('h4o_2022_data.csv')
data.head()

import folium

# base map
m = folium.Map(location=[data['lat'].mean(), data['lon'].mean()], zoom_start=10)

# Add markers for each coordinate
for lat, lon in zip(data['lat'], data['lon']):
    folium.CircleMarker(
        location=[lat, lon],
        radius=3,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.6
    ).add_to(m)

#Displayx
m.save("index.html")
display(m)



