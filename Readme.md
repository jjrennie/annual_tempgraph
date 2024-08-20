# Annual Temperature Graphs
## Written By Jared Rennie (@jjrennie)

In this notebook, you will learn how to make an annual temperature graph, much like one you see <a href='https://twitter.com/jjrennie/status/1728857989464179169' target="_blank">here</a>

We will utilize a stations maximum and minimum temperature for it's period of record. While we are only highlighting a specific year, we can utilize the period of record to get other useful information, like extremes and normals. Data originates from <a href='https://www.ncei.noaa.gov' target="_blank">NOAA NCEI</a>, who holds all of the worlds weather data. This code will show you how to access the data via an API, clean it up some, and plot a pretty graphic. 

### What You Need

First off, the entire codebase works in Python 3. In addition to base Python, you will need the following packages installed: 
- requests (to access the api)
- pandas (to slice annd dice the data)
- matplotlib (to plot!)
    
The "easiest" way is to install these is by installing <a href='https://www.anaconda.com' target="_blank">anaconda</a>, and then applying <a href='https://conda-forge.org/' target="_blank">conda-forge</a>. Afterward, then you can install the above packages. 

### Launch right now with binder
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jjrennie/annual_tempgraph/HEAD?labpath=plot_tempgraph.ipynb)
