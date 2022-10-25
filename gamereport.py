#!/usr/bin/python3
import datetime
import sys
from optparse import OptionParser

seas_start = datetime.datetime(2022,5,2)
seas_end =  datetime.datetime(2022,7,29)

def get_options():
    """
    Purpose: Processes options and allows for further option interrogation.
    """

    p = OptionParser()
    p.add_option( "-l", "--league", action="store", type="string", dest="league", default="all",
                  help="Name of league" )
    p.add_option( "-t", "--tens", action="store_true", dest="tens", default=False,
                  help="Show the 10pm game count" )
    p.add_option( "-s", "--summary", action="store_true", dest="summary", default=False,
                  help="Show the game summary" )
    p.add_option( "-n", "--teams", action="store", type="string", dest="teams", default="",
                  help="List of teams, comma separated (ex:  -n Legion,Mingos,317" )
    options,args = p.parse_args()

    # Options Handlers
    return options,args

def main(args):
    opts,args = get_options()
    allleagues = ['CoedE1', 'CoedE2', 'CoedE3', 'MensCD', 'MensE1', 'MensE2' ]
    mensleagues = ['MensCD', 'MensE1', 'MensE2' ]
    coedleagues = ['CoedE1', 'CoedE2', 'CoedE3', 'MensCD', 'MensE1', 'MensE2' ]
    gamecount = 0

    optsleag = opts.league.lower()
    if optsleag == 'all':
        leagues = allleagues
    elif optsleag == 'list':
        print("Available leagues:")
        for each in allleagues:
            print("\t%s" % each)
        sys.exit()
    elif optsleag == 'coede1':
        leagues = ['CoedE1']
    elif optsleag == 'coede2':
        leagues = ['CoedE2']
    elif optsleag == 'coede3':
        leagues = ['CoedE3']
    elif optsleag == 'menscd':
        leagues = ['MensCD']
    elif optsleag == 'mense1':
        leagues = ['MensE1']
    elif optsleag == 'mense2':
        leagues = ['MensE2']
    elif optsleag == 'mense':
        leagues = ['MensE1', 'MensE2']
    else:
        print("Error no such league: %s" % opts.league)
        sys.exit()
        
    games = { 'CoedE1': {}, 'CoedE2': {}, 'CoedE3': {}, 'MensCD': {}, 'MensE1': {}, 'MensE2': {} , 'MensE': {} }
    tenpmgames={}

    f = open("mastersched.csv", "r")
    lines = f.readlines()
    for line in lines:
        gamecount += 1
        c_fields = line.split(",")

        league = c_fields[0]

        month = c_fields[1][4:5] 
        day = c_fields[1].split("/")[1]

        time = c_fields[2][0]

        t1 = c_fields[3]
        t2 = c_fields[4]
        field = c_fields[5][6:7]


        slotname = "%s/%s:%s|%s" %(month, day, time, field)

        # add an entry for each team
        if t1 not in games[league]:
            games[league][t1] = []
        if slotname not in games[league][t1]:
            games[league][t1].append(slotname)
        else:
            print("ERROR: Duplicate slot")
            print(line)

        if t2 not in games[league]:
            games[league][t2] = []
        if slotname not in  games[league][t2]:
            games[league][t2].append(slotname)
        else:
            print("ERROR: Duplicate slot")
            print(line)

        if league == 'MensE1' or league == 'MensE2':
            # add to combined mens e 
            if t1 not in games['MensE']:
                games['MensE'][t1] = []
            if slotname not in games['MensE'][t1]:
                games['MensE'][t1].append(slotname)
            else:
                print("ERROR: Duplicate slot")
                print(line)
            if t2 not in games['MensE']:
                games['MensE'][t2] = []
            if slotname not in  games['MensE'][t2]:
                games['MensE'][t2].append(slotname)
            else:
                print("ERROR: Duplicate slot")
                print(line)

        t1name = "%s %s" %(league,t1)
        t2name = "%s %s" %(league,t2)
        if t1name not in tenpmgames:
            tenpmgames[t1name] = 0
        if t2name not in tenpmgames:
            tenpmgames[t2name] = 0
        if time == "1":
            tenpmgames[t1name] += 1
            tenpmgames[t2name] += 1

    if opts.tens:
        tenlist = sorted(tenpmgames.items(), key=lambda x:x[1])
        for i in range(0, len(tenlist)):
            if tenlist[i][1] == 0: continue
            print("%i  %s" % (tenlist[i][1], tenlist[i][0]))
        sys.exit()

    if opts.summary:
        print("\nCoed E1 Teams: %i" % len(games['CoedE1']))
        print("Coed E2 Teams: %2i" % len(games['CoedE2']))
        print("Coed E3 Teams: %2i" % len(games['CoedE3']))
        print("Mens CD Teams: %2i" % len(games['MensCD']))
        print("Mens E1 Teams: %2i" % len(games['MensE1']))
        print("Mens E2 Teams: %2i" % len(games['MensE2']))
        print("Womens  Teams: 0" )
        print("  Total Teams: %2i" % (len(games['CoedE1'])+len(games['CoedE2'])+len(games['CoedE3'])+len(games['MensCD'])+len(games['MensE1'])+len(games['MensE2'])))
        print("\nTotal Games: %i\n" % gamecount)
        sys.exit()

    print("+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+")
    print("               |      5/2      |      5/9      |      5/16     |      5/23     |      5/30     |      6/6      |      6/13     |      6/20     |      6/27     |      7/4      |      7/11     |      7/18     |      7/22     |")
    print("               |2  3  4  5  6  |9  10 11 12 13 |16 17 18 19 20 |23 24 25 26 27 |30 31 1  2  3  |6  7  8  9  10 |13 14 15 16 17 |20 21 22 23 24 |27 28 29 30 1  |4  5  6  7  8  |11 12 13 14 15 |18 19 20 21 22 |25 26 27 28 29 |")
    print("               |M  T  W  T  F  |M  T  W  T  F  |M  T  W  T  F  |M  T  W  T  F  |M  T  W  T  F  |M  T  W  T  F  |M  T  W  T  F  |M  T  W  T  F  |M  T  W  T  F  |M  T  W  T  F  |M  T  W  T  F  |M  T  W  T  F  |M  T  W  T  F  |")
    print("---------------+---------------+===============+---------------+===============+---------------+===============+---------------+===============+---------------+===============+---------------+===============+---------------|")


    for league in leagues:
        for team in games[league]:
            
            if opts.teams:
                teamlist = opts.teams.split(',')
                skip = False
                for each in teamlist:
                    if each not in team:
                        skip = True
                    else:
                        skip = False
                        break
                if skip: continue

            sys.stdout.write("%i %-11s |" % (len(games[league][team]), team[0:11]))

            day = seas_start
            while day <= seas_end:
                output = ""
                for time in ["6", "7", "8", "1"]:
                    for field in ["1", "2", "3", "4", "5"]:
                        slotname = "%s:%s|%s" % (day.strftime("%-m/%-d"), time, field)
    
                        if slotname in games[league][team]:
                            output = output+time
    
                sys.stdout.write("%-3s" % output)
            
                dayinc=1
                if day.strftime("%a") == "Fri":
                    sys.stdout.write("|")
                    dayinc = 3
                day =  day + datetime.timedelta(days=dayinc)
    
            sys.stdout.write("\n")

        if not opts.teams:
            print("-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+")
    print("")
    




if __name__=='__main__':
    main(sys.argv)
