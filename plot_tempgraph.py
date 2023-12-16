# Written By Jared Rennie 

# Import packages
import json,requests,sys,calendar
import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# Read in Arguments 
if len(sys.argv) < 3:
    sys.exit("USAGE: <ID> <YEAR>\n Example: python plot_tempgraph.py AVL 2023")  
stationID = sys.argv[1]
plotYear= int(sys.argv[2])

# Other Arguments that can be changed
author='Jared Rennie (@jjrennie)'
dpi=300
normals_start=1991
normals_end=2020

# Build JSON to access ACIS API (from https://www.rcc-acis.org/docs_webservices.html)
acis_url = 'http://data.rcc-acis.org/StnData'
payload = {
"output": "json",
"params": {"elems":[{"name":"maxt","interval":"dly","prec":1},
                    {"name":"mint","interval":"dly","prec":1},
                    {"name":"maxt","interval":"dly","normal":"1","prec":1},
                    {"name":"mint","interval":"dly","normal":"1","prec":1}],
           "sid":stationID,
           "sdate":"por",
           "edate":"por"
          } 
}

# Make Request
try:
    r = requests.post(acis_url, json=payload,timeout=3)
    acisData = r.json()
except Exception as e:
    sys.exit('\nSomething Went Wrong With Accessing API after 3 seconds, Try Again')

# Get Station Info
stationName=acisData['meta']['name'].title()
stationState=acisData['meta']['state']
print("\nSuccessfully Got Data for: ",stationName,'\n')

# Convert Data to Pandas, get start and end year
acisPandas = pd.DataFrame(acisData['data'], columns=['Date','TmaxVal','TminVal','TmaxNormal','TminNormal'])
stationStart=acisPandas.iloc[[0]]['Date'].values[0][0:4]
stationEnd=acisPandas.iloc[[-1]]['Date'].values[0][0:4]

# Remove Missing Data And Reformat Each Column
for (columnName, columnData) in acisPandas.items():
    acisPandas = acisPandas[acisPandas[columnName] != 'M']
    if columnName == 'Date':
        acisPandas[columnName] = pd.to_datetime(acisPandas[columnName])
    else:
        acisPandas[columnName] = pd.to_numeric(acisPandas[columnName])
lastDate=acisPandas.iloc[-1]['Date']

# Get Extremes of Tmax/Tmin for each day
acisPandas['Year'] = acisPandas['Date'].dt.year
acisPandas['DayOfYear'] = acisPandas['Date'].dt.dayofyear
acisExtremes1 = acisPandas.groupby(['DayOfYear']).agg({'TmaxVal': 'max', 'TminVal': 'min'}).reset_index()
acisExtremes2 = acisPandas.groupby(['DayOfYear']).agg({'TmaxVal': 'min', 'TminVal': 'max'}).reset_index()

# Get Data for Year Given as Input, and take care of leap day.
# Also need a full year for plotting other data, so use a complete year (ie 2020)
plotData=acisPandas[acisPandas['Year']==plotYear].reset_index(drop=True)
normalData=acisPandas[acisPandas['Year']==2016]

if not calendar.isleap(plotYear):
    acisExtremes1=acisExtremes1.drop(acisExtremes1[acisExtremes1['DayOfYear'] == 60].index).reset_index(drop=True)
    acisExtremes1['DayOfYear'] = range(1, 366)

    acisExtremes2=acisExtremes2.drop(acisExtremes2[acisExtremes2['DayOfYear'] == 60].index).reset_index(drop=True)
    acisExtremes2['DayOfYear'] = range(1, 366)

    normalData=normalData.drop(normalData[normalData['DayOfYear'] == 60].index).reset_index(drop=True)
    normalData['DayOfYear'] = range(1, 366)

# Find Days in the plot year that either tied or broke a record.
highMax = plotData[plotData['TmaxVal'] >= acisExtremes1[0:len(plotData)]['TmaxVal']]
lowMin = plotData[plotData['TminVal'] <= acisExtremes1[0:len(plotData)]['TminVal']]
lowMax = plotData[plotData['TmaxVal'] <= acisExtremes2[0:len(plotData)]['TmaxVal']]
highMin = plotData[plotData['TminVal'] >= acisExtremes2[0:len(plotData)]['TminVal']]

#################################################
# PLOT
print("PLOTTING")

# Set up the plot
fig, axf = plt.subplots(figsize=(15, 8), edgecolor='white', facecolor='white', dpi=dpi)
plt.style.use("dark_background")

# Add grid lines
plt.grid(color='white', linestyle='--', linewidth=0.5, alpha=0.3)
axf.set_facecolor('#808080')

# Plot Record TMAX/TMIN
plt.bar(acisExtremes1['DayOfYear'], acisExtremes1['TmaxVal'] - acisExtremes1['TminVal'], bottom=acisExtremes1['TminVal'], edgecolor='none', color='#c3bba4', width=1, label="Record Max/Min Range")

# Plot Normal TMAX/TMIN
plt.bar(normalData['DayOfYear'], normalData['TmaxNormal'] - normalData['TminNormal'], bottom=normalData['TminNormal'], edgecolor='none', color='#9a9180', width=1, label="Average ("+str(normals_start)+"-"+str(normals_end)+") Max/Min Range")

# Plot Raw TMAX/TMIN
plt.plot(plotData['DayOfYear'], plotData['TmaxVal'], linewidth=2, color='#D6604D', label="Daily Max")
plt.plot(plotData['DayOfYear'], plotData['TminVal'], linewidth=2, color='#4393C3', label="Daily Min")

# Plot New Max/Min Records
plt.scatter(highMax['DayOfYear'], highMax['TmaxVal'] + 0.50, s=35, zorder=10, color='#B2182B', alpha=1, edgecolor='black', linewidth=0.75, label="New/Tied Highest Max ("+str(len(highMax))+")")
plt.scatter(lowMin['DayOfYear'], lowMin['TminVal'] - 0.50, s=35, zorder=10, color='#2166AC', alpha=1, edgecolor='black', linewidth=0.75, label="New/Tied Lowest Min ("+str(len(lowMin))+")")
plt.scatter(lowMax['DayOfYear'], lowMax['TmaxVal'] + 0.50, s=35, zorder=10, color='cyan', alpha=1, edgecolor='black', linewidth=0.75, label="New/Tied Lowest Max ("+str(len(lowMax))+")")
plt.scatter(highMin['DayOfYear'], highMin['TminVal'] - 0.50, s=35, zorder=10, color='#FEB24C', alpha=1, edgecolor='black', linewidth=0.75, label="New/Tied Highest Min ("+str(len(highMin))+")")

# Plot Legend
plt.legend(bbox_to_anchor=(0., -.137, 1., -1.02), loc=3, ncol=4, mode="expand", borderaxespad=0., fontsize=12, facecolor='#808080')

# Set X/Y limits
ymin=int(5 * round(float((min(acisExtremes1['TminVal']) - 10))/5))
ymax=int(5 * round(float((max(acisExtremes1['TmaxVal']) + 10))/5))
plt.ylim(ymin, ymax)
plt.xlim(-5, 366) 

# Plot X-Axis Labels/Ticks
month_pos=[1,32,60,91,121,152,182,213,244,274,305,335]
month_names=["Jan 1","Feb 1","Mar 1","Apr 1","May 1","Jun 1","Jul 1","Aug 1","Sep 1","Oct 1","Nov 1","Dec 1"]
plt.xticks(month_pos, month_names, fontsize=12, color='white')

# Plot Y-Axis Labels/Ticks (Left Side, degF)
plt.yticks(range(ymin, ymax, 10), [r'{}'.format(x) for x in range(ymin, ymax, 10)], fontsize=12, color='white')
plt.ylabel(r'Temperature (°F)', fontsize=15, color='white')

# Plot Y-Axis Labels/Ticks (Right Side, degC)
ymax=int((ymax-32) / 1.8)
ymin=int((ymin-32) / 1.8)
axc = axf.twinx()
y1, y2 = axf.get_ylim()
axc.set_ylim(int((y1-32) / 1.8), int((y2-32) / 1.8))
axc.figure.canvas.draw()
axf.callbacks.connect("ylim_changed", axc)
axc.set_ylabel(r'Temperature (°C)', fontsize=15, rotation=270, labelpad=20)

# Plot Title/Subtitle/Annotations
plt.suptitle(str(plotYear)+' Temperatures For '+stationName+', '+stationState, fontsize=17,color='white')
plt.title('Station ID: '+stationID+' | Period of Record: '+str(stationStart)+'-'+str(stationEnd), fontsize=13,color='white')
plt.annotate('Source: ACIS | Generated by '+author+' | Data up to '+lastDate.strftime('%Y-%m-%d'),xy=(0.995, 0.01), xycoords='axes fraction', fontsize=7,horizontalalignment='right', verticalalignment='bottom')

# Save and Close
plt.savefig('./'+stationID+'_tempgraph_'+str(plotYear)+'.png', dpi=dpi,bbox_inches='tight')
plt.clf()
plt.close()

# Done! Close Program
print('DONE!')
sys.exit()