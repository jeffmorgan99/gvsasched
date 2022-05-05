#!/usr/bin/python3
import datetime
import sys
import pandas as pd

master = "mastersched.csv"

# urls
urls = [ 'CoedE1|https://gvsoftball.org/schedule/383211/coed-e1',
         'CoedE2|https://gvsoftball.org/schedule/383212/coed-e2',
         'CoedE3|https://gvsoftball.org/schedule/383213/coed-e3',
         'MensCD|https://gvsoftball.org/schedule/383208/mens-cd',
         'MensE1|https://gvsoftball.org/schedule/393203/mens-emasters-division-1',
         'MensE2|https://gvsoftball.org/schedule/383207/mens-emasters-division-2'
         ]

ms = open(master, "w")
mense = open("MensE.sched.csv", "w")

for each in urls:
    leag = each.split("|")[0]
    url = each.split("|")[1]

    print("Working on %-6s [%s]" %(leag, url))
    df = pd.read_html(url)

    f = open("%s.sched.csv" %leag, "w")
    print("Writing to file [%s.sched.csv]" % leag)

    for i in range(0,len(df[2]['Time'])):
        if type(df[2]['Date'][i]) != str: continue
        if df[2]['Date'][i][0:4] == 'Week': continue
        f.write("%s,%s,%s,%s,%s,%s\n" %(leag,df[2]['Date'][i],df[2]['Time'][i],df[2]['Home'][i],df[2]['Away'][i],df[2]['Location'][i]))
        ms.write("%s,%s,%s,%s,%s,%s\n" %(leag,df[2]['Date'][i],df[2]['Time'][i],df[2]['Home'][i],df[2]['Away'][i],df[2]['Location'][i]))

        if leag == "MensE1":
            mense.write("%s,%s,%s,%s,%s,%s\n" %(leag,df[2]['Date'][i],df[2]['Time'][i],df[2]['Home'][i],df[2]['Away'][i],df[2]['Location'][i]))
        if leag == "MensE2":
            mense.write("%s,%s,%s,%s,%s,%s\n" %(leag,df[2]['Date'][i],df[2]['Time'][i],df[2]['Home'][i],df[2]['Away'][i],df[2]['Location'][i]))

    f.close()


ms.close()
mense.close()
