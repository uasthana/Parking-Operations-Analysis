"""The program calculates the average IN and OUT time of a card user, calculates the confidence 
   interval and lists the number of outliers for each card user"""
import pandas as pd
import numpy as np
from scipy import stats as  sp
import os

df = pd.read_csv(r'C:\Utkarsh\GIT\Python\ParkingRevenueAnalysis\Data.csv')#INSERT DATA FILE PATH
df = df[df['Result'] == 'Valid Access']

np_cardnumber = df['Card Number'].values.tolist()
np_cardnumber =np.unique(np_cardnumber)

file = open(os.path.expanduser(r"C:\Utkarsh\GIT\Python\ParkingRevenueAnalysis\Result.csv"), "wb")#INSERT RESULT FILE PATH
file.write(b"CardNumber,Intime_mean,Intime_conf_int,Intime_outliers,Total_Ins,Outtime_mean,Outtime_conf_int,Outtime_outliers,Total_Outs"+b"\n") 

for x in range(0,len(np_cardnumber)):
    df_cardnumber = df[df['Card Number'] == np_cardnumber[x]]
    df_in = df_cardnumber[df_cardnumber['Direction']=='In']
    df_out = df_cardnumber[df_cardnumber['Direction']=='Out']
    np_in = df_in[['Direction','Date and Time']].values.tolist()
    np_out = df_out[['Direction','Date and Time']].values.tolist()
    t_in=[]
    t_out=[]
    for y_in in range(0,len(np_in)):
        k_in= np_in[y_in][1].split()[1]
        hour_in=int(k_in.split(":")[0])
        minute_in=int(k_in.split(":")[1])
        timeofday_in = hour_in*60 + minute_in   
        t_in.append(timeofday_in)
        t_mean_in = np.mean(t_in)
        t_std_in = np.std(t_in)
        conf_int_in = sp.norm.interval(.68, loc=t_mean_in, scale=t_std_in )
        total_in = len(t_in)
        c_in=0
        for z_in in range(0,len(t_in)):
            if(t_in[z_in]< conf_int_in[0]):
                c_in = c_in+1
            elif(t_in[z_in]>conf_int_in[1]):
                c_in = c_in+1    
    for y_out in range(0,len(np_out)):
        k_out = np_out[y_out][1].split()[1]
        hour_out = int(k_out.split(":")[0])
        minute_out = int(k_out.split(":")[1])
        timeofday_out = hour_out*60 + minute_out
        t_out.append(timeofday_out)
        t_mean_out = np.mean(t_out)
        t_std_out = np.std(t_out)
        conf_int_out = sp.norm.interval(.68, loc=t_mean_out, scale=t_std_out)
        total_out = len(t_out)
        c_out=0
        for z_out in range(0,len(t_out)):
            if((t_out[z_out])<conf_int_out[0]):
                c_out = c_out+1
            elif(t_out[z_out]>conf_int_out[1]):
                c_out = c_out+1
    
    if(len(df_in)>5):
        div = int(t_mean_in/60)
        rem = int(t_mean_in%60)
        intime_mean = str(div)+":"+str(rem)            
        div1 = int(conf_int_in[0]/60)
        rem1 = int(conf_int_in[0]%60)
        div2 = int(conf_int_in[1]/60)
        rem2 = int(conf_int_in[1]%60)
        intime_conf_int = str(div1)+":"+str(rem1)+" - "+str(div2)+":"+str(rem2)
        
    elif(len(df_in)<5 and len(df_in)>0):
        div = int(t_mean_in/60)
        rem = int(t_mean_in%60)
        intime_mean = str(div)+":"+str(rem)
        intime_conf_int = 'N\A'
        
    else:
        intime_mean = 'N\A'
        intime_conf_int = 'N\A'
        
    if(len(df_out)>5):
        div = int(t_mean_out/60)
        rem = int(t_mean_out%60)
        outtime_mean = str(div)+":"+str(rem)  
        div1 = int(conf_int_out[0]/60)
        rem1 = int(conf_int_out[0]%60)
        div2 = int(conf_int_out[1]/60)
        rem2 = int(conf_int_out[1]%60)
        outtime_conf_int = str(div1)+":"+str(rem1)+" - "+str(div2)+":"+str(rem2)
        
    elif(len(df_out)<5 and len(df_out)>0):
        div = int(t_mean_out/60)
        rem = int(t_mean_out%60)
        outtime_mean = str(div)+":"+str(rem)
        outtime_conf_int = 'N\A'
        
    else:
        outtime_mean = 'N\A'
        outtime_conf_int = 'N\A'
        
    combinedstring = str(np_cardnumber[x]) + "," + str(intime_mean) + "," + str(intime_conf_int) + "," + str(c_in)+ "," + str(total_in) + "," + str(outtime_mean) + "," + str(outtime_conf_int) + "," + str(c_out)+ "," + str(total_out) + "\n"
    file.write(bytes(combinedstring, encoding="ascii", errors='ignore'))            
    print(combinedstring)

file.close()

