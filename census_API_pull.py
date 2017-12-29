'''
Pull in Census information from a Python API via the Census package.
Data will be pulled and then written out to a CSV file.

David Rose 2017-12-14
'''
from census import Census
from us import states
import numpy as np
import pandas as pd

# API access key, simple to obtain. Just check census site, API section
key = Census('7b0a735fdb7a8856b045f744c61a1480a6947b10')

# CSV file created manually to obtain API codes for each metric
age_race_codes = pd.read_csv('age_race_codes.csv')
print('Loaded codes for Age/Sex/Race population. \n----------------------\n')

################
## Main loop to cycle through each code in the CSV file and pull all counties
################

# First get all the counties
# County can be changed to another hierarchy
# Currently pulls one state at a time (AL) can be modified to loop thru all
for i in range(age_race_codes.shape[0]):
    print('Current Metric: ',age_race_codes['metric'][i])
    codes = key.acs5.get(
        #print('for','zip5:*', 'in','state:{}')
        ('NAME', age_race_codes['code2'][i]),
        {'for':'County:*', 'in':'state:{}'.format(states.AL.fips)})
    #print('County: ',codes[i]['NAME'])
    #print('Value: ',codes[i][age_race_codes['code2'][i]])
    
    # If first row
    if i == 0:
        # Create the empty PD DF to attach results iteratively
        df = pd.DataFrame(np.zeros(0,dtype=[
            ('County', 'a50'),
            ('Metric', 'a50'),
            ('Value',  'i8')]))

    
    # Begin compiling the data from the API to a DF
    ii = 0
    for code in range(len(codes)):
        #print('for metric: ', age_race_codes['metric'][i])
        print('The county is: ',codes[code]['NAME'])
        print('value is: ', codes[code][age_race_codes['code2'][i]])
        
        #column[codes[code]['NAME']] = codes[code][age_race_codes['code2'][i]]
        #column.append(codes[i][age_race_codes['code2'][i]])
        
        # Add this all up to a final pandas DF
        df = df.append({'County':codes[code]['NAME'],
                        'Metric':age_race_codes['metric'][i],
                        'Value' :codes[code][age_race_codes['code2'][i]]}
                       ,ignore_index=True)
        
        # To stop after n counties - Debugging purposes
        #if ii > 10:
        #    print("got 10")
        #    break
        #ii = ii + 1
    

print('Final dataframe size is: ',df.shape)

df.to_csv('Census_Data.csv')    

        
    

