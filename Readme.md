# Annual Temperature Graphs
## Written By Jared Rennie (@jjrennie)

In this notebook, you will learn how to make an annual temperature graph, much like one you see <a href='https://twitter.com/jjrennie/status/1728857989464179169' target="_blank">here</a>:

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">A month in left in 2023, but Ely, Nevada and Little Rock, Arkansas currently have the coldest and warmest stations in the United States, when looking at anomalies (departure from their 1991-2020 means). <br><br>Ely, NV: -3.1F<br>Little Rock: +4.5F<a href="https://twitter.com/hashtag/NVwx?src=hash&amp;ref_src=twsrc%5Etfw">#NVwx</a> <a href="https://twitter.com/hashtag/ARwx?src=hash&amp;ref_src=twsrc%5Etfw">#ARwx</a> <a href="https://t.co/iSxhwNoCkX">pic.twitter.com/iSxhwNoCkX</a></p>&mdash; Jared Rennie (@jjrennie) <a href="https://twitter.com/jjrennie/status/1728857989464179169?ref_src=twsrc%5Etfw">November 26, 2023</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

We will utilize a stations maximum and minimum temperature for it's period of record. While we are only highlighting a specific year, we can utilize the period of record to get other useful information, like extremes and normals. Data originates from <a href='https://www.ncei.noaa.gov' target="_blank">NOAA NCEI</a>, who holds all of the worlds weather data. This code will show you how to access the data via an API, clean it up some, and plot a pretty graphic. 

### What You Need

First off, the entire codebase works in Python 3. In addition to base Python, you will need the following packages installed: 
- requests (to access the api)
- pandas (to slice annd dice the data)
- matplotlib (to plot!)
    
The "easiest" way is to install these is by installing <a href='https://www.anaconda.com' target="_blank">anaconda</a>, and then applying <a href='https://conda-forge.org/' target="_blank">conda-forge</a>. Afterward, then you can install the above packages. 