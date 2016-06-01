"""The program calculates the total occupancy of the garage at each hour of day range given"""
import pandas as pd
from datetime import datetime,timedelta
import os

df = pd.read_csv(r'C:\Utkarsh\GIT\Python\ParkingRevenueAnalysis\Occupancy.csv')#INSERT DATA FILE PATH
#print(df)

df_entry = df[['Ticket Number','Ticket Type','Transaction Type','Entrance Date and Time','Exit Date and Time']]

df_entry = df_entry[(df_entry['Ticket Type'] == 'Entry') & (df_entry['Transaction Type'] == 'Normal')]
np = df_entry.values.T.tolist()
#Day Range
starttime  = '12/01/2015 12:00 AM'
endtime = '02/29/2016 11:59 PM'
date1 = datetime.strptime(starttime, '%m/%d/%Y %I:%M %p')
date2 = datetime.strptime(endtime, '%m/%d/%Y %I:%M %p')

file = open(os.path.expanduser(r"C:\Utkarsh\GIT\Python\ParkingRevenueAnalysis\OccupancyPerHour.csv"), "wb")#INSERT RESULT FILE PATH
file.write(b"TimeOfDay,TotalCars"+b"\n") 

numhours = int(round((date2-date1).seconds/3600+(date2-date1).days*24,0)+1)
for timeofday in range(1,numhours):
    count = 0
    for x in range (len(np[1])):
        if((datetime.strptime((np[3][x]).strip(), '%m/%d/%Y %I:%M %p') <= date1) and (datetime.strptime((np[4][x]).strip(), '%m/%d/%Y %I:%M %p') >= date1)):
            count =count+1
    combinedstring = str(date1) + "," + str(count) + "\n"
    file.write(bytes(combinedstring, encoding="ascii", errors='ignore'))
    date1 = date1+timedelta(hours=1)
    print(combinedstring)
file.close()



