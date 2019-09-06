import json
import iso3166
import yaml

with open('regions.json', 'r') as JSON:
       data = json.load(JSON)

reg_iso = list(data)
print(reg_iso)
#print(reg_iso)
skipped = []
dict1 = {} # dictionary of names and their iso
for j in reg_iso:
    try: 
        # Get name
        name = iso3166.countries_by_alpha3[j].name.lower() 
        dict1[j] = name
        # Export to .yaml file
        with open('iso.yaml', 'w') as yaml_file:
            yaml.dump(dict1, yaml_file, default_flow_style=False)
        
    except Exception:
        #skipped.append(j)
        pass

#print(skipped) #'ANT' cannot find name error



