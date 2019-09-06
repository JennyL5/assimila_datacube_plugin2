import json
import iso3166
import yaml

with open('regions.json', 'r') as JSON:
       data = json.load(JSON)

reg_iso = list(data)
#print(reg_iso)
skipped = []
dict1 = {} # dictionary of names and n,e,s,w
dict2 = {} # dictionary of n,e,s,w
for j in reg_iso:
    try: 
        north = data[j]['ne']['lat']
        east = data[j]['ne']['lon']
        south = data[j]['sw']['lat']
        west = data[j]['sw']['lon']

        # Get name
        name = iso3166.countries_by_alpha3[j].name.lower() 
        #print(f"name: %s, alpha3: %s, north: %d, east: %d, south: %d, west: %d" % (name, j, north, east, south, west))

        # Create dictionary within dictionary
        dict2 = {'south': south, 'north': north, 'west': west, 'east': east}
        dict1[name] = dict2
        #print(dict1)
        
        # Export to .yaml file
        with open('DQTools/DQTools/regions/regions.yaml', 'w') as yaml_file:
            yaml.dump(dict1, yaml_file, default_flow_style=False)
        
    except Exception:
        skipped.append(j)
        pass

print(skipped) #'ANT' cannot find name error