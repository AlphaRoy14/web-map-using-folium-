import folium
import pandas

map=folium.Map(location=[23,89],zoom_start=6,tiles="Mapbox Bright")

#map.add_child(folium.Marker(location=[23,89],popup="Home",icon=folium.Icon(color="green")))

#add_child updates the objet it self just like how append upates the list object

'''We added a add_child method to make it a child of the object and so that itr can be layered on top'''
''' The above step has been commented because its better to make a future group object and pass it to a map child later
in this way we can have many featured and can also have an option of turning them off as desired by the user in the program'''

#adding a marker to the map
fg=folium.FeatureGroup(name="My HOME")

fgv=folium.FeatureGroup(name="My volcanos")
fg.add_child(folium.Marker(location=[23,89],popup="Home",icon=folium.Icon(color="green"))) #Making a child of  the object
fg.add_child(folium.Marker(location=[24,10],popup="Not my Home",icon=folium.Icon(color="blue"))) #Making a child of  the object
#multiple marker

'''can make the multiple markers by using a forloop aswell '''
# for coordinates in [[23,89],[24,10]]:
    # fg.add_child(folium.Marker(location=coordinates,popup="Home",icon=folium.Icon(color="green")))


'''Reading from a csv'''

data=pandas.read_csv("Volcanoes_USA.txt")
lon=list(data["LON"])
lat=list(data["LAT"])
name_of_vol=list(data["NAME"])
Elev=list(data["ELEV"])
#to iterate through lon and lat at the same  time we need to use the function zip
'''zip basically goies like ----> for i ,j in zip ([1,2,3],[5,6,7]) : it'll choose i and j as 1 and 5 simultaneously '''

def colour_producer(elevation):
    if elevation <1000:
        return "green"
    elif elevation<2500:
        return "blue"
    else:
        return "red"
fgp=folium.FeatureGroup(name="population")

for lt , ln ,el in zip(lat,lon,Elev):
    fgv.add_child(folium.Marker(location=[lt,ln],popup=folium.Popup(str(el)+" m",parse_html=True),icon=folium.Icon(color=colour_producer(el)))) #Making a child of  the object
    # we see that for popup we had to use folium.popup and or else with direct string the screen was blank. this is because some of the name had an ' which kind of
    # spoils the html code .. so in order to fix that we needed to use the folium.popup Also remember popup takes str valus and not numeric
fgp.add_child(folium.GeoJson(data=open("world.json",'r',encoding='utf-8-sig').read(),
style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005']<1000000 else 'orange' if 20000000>x['properties']['POP2005']>=10000000 else "red"})) #encoding was required idk why and on the lastes version of folium we need to read the
                    #geojson file so that its in string format hence the .read()

# the style_function is used to add colour to the map polygon and its a bit difficult tio logically interpret that is because of the internal code of folium
# so the dont stress about what and why. and folium turns python code into javascript code so thats why we are passing colourfill as a dictionary type. As it'd be easir to
# convert that into a javascript code

'''GeoJson is a type of jason which helps create polygon, lines and points with the help of coordinated for further info: https://en.wikipedia.org/wiki/GeoJSON'''
""">>> y = lambda x: {'fillColor':'green' if x>0 else 'red'}
>>> y(1)
{'fillColor': 'green'} #understanding lanbda better
>>> y(-1)
{'fillColor': 'red'}"""



map.add_child(fg)
map.add_child(fgv)
map.add_child(fgp)

map.add_child(folium.LayerControl())  # *must be added below the featurGroup or else it wont be visible
#it checks for all the add_childs of the map object above and make a layer control of each
map.save("map1.html")
