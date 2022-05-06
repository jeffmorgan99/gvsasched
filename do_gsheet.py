#!/usr/bin/python3
"""
pythongooglesheets-119@testsched.iam.gserviceaccount.com


"""
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import json
import datetime
import sys
from optparse import OptionParser
import time

def get_options():
    """
    Purpose: Processes options and allows for further option interrogation.
    """

    p = OptionParser()
    p.add_option( "-d", "--date", action="store", type="string", dest="date", default=False,
            help="Pass the Monday you want to start on: MM/DD/YY (5/9/22)" )
    options,args = p.parse_args()

    # Options Handlers
    return options,args


if __name__=='__main__':
    opts,args = get_options()

    seas_start = datetime.datetime(2022,5,2)
    seas_end =  datetime.datetime(2022,7,29)
    template_name = "2022 Schedule Sheets Template"

    if opts.date:
        try:
            sheet_date = datetime.datetime.strptime(opts.date, '%m/%d/%y')
            if sheet_date.strftime("%a") != 'Mon':
                print("Must pass a Monday only")
                sys.exit()
        except:
            print("Error parsing date passed")
            sys.exit()
    else:
        today = datetime.datetime.now()
        # if today is Tuesday or later, assume you want next week's sheets
        if today.strftime("%a") == "Tue":
            sheet_inc = 6
        elif today.strftime("%a") == "Wed":
            sheet_inc = 5
        elif today.strftime("%a") == "Thu":
            sheet_inc = 4
        elif today.strftime("%a") == "Fri":
            sheet_inc = 3
        elif today.strftime("%a") == "Sat":
            sheet_inc = 2
        elif today.strftime("%a") == "Sun":
            sheet_inc = 1
        sheet_date = today + datetime.timedelta(days=sheet_inc)

    sheet_name = sheet_date.strftime("%Y-%m-%d") + " Schedule Sheets"
    print("Using starting Monday [%s]" % sheet_date.strftime("%a %m/%d/%Y"))

    try:
        scopes = [ 'https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive' ]
        credentials = ServiceAccountCredentials.from_json_keyfile_name("testsched-4b1a8ed19321.json", scopes)
        client = gspread.authorize(credentials)
    except:
        print("Unable to google sheet")
        sys.exit()

    # First check if sheet already exists
    print("Checking for existing Google Drive sheet [%s]" % sheet_name)
    try:
        sheet = client.open(sheet_name)
        ssbull= sheet.sheet1
        open_sheet = True
    except:
        print("Could not open sheet [%s]" % sheet_name)
        open_sheet = False

    if open_sheet:
        # sanity check date
        if ssbull.acell('A1').value != sheet_date.strftime("%A, %B %d, %Y"):
            print("sheet name check failed")
            print("[%s] != [%s]" %(ssbull.acell('A1').value, sheet_date.strftime("%A, %B %d, %Y")))
            sys.exit()
        print("[%s] == [%s]" %(ssbull.acell('A1').value, sheet_date.strftime("%A, %B %d, %Y")))
    else:
        print("Creating Google Sheet from template")
        client.copy("1xtl_IDUqblQ-LFb2RXOtU35pGGi81dd6m8VAm2UTN6Y", title=sheet_name, folder_id="1xkNS8kKOqp9y6mkUcBkYw4iSgdProsTA", copy_permissions=True)
        ss = client.open(sheet_name)
        ss.share("pythongooglesheets-119@testsched.iam.gserviceaccount.com", perm_type='user', role='writer')
        ssbull = ss.sheet1
        #print(ssbull.acell('A1').value)

    # populate data structure
    # games {  'date' : { 'field' : { 'time' : [ 'team 1', 'team 2' ] } } }
    games = {}
    for dayinc in range(0,5):
        working_date = sheet_date + datetime.timedelta(days=dayinc)
        games[working_date.strftime("%a %-m/%-d")] = {}
        for field in [1, 2, 3, 4, 5]:
            games[working_date.strftime("%a %-m/%-d")][field] = {}

            for tme in [6, 7, 8, 10]:
                games[working_date.strftime("%a %-m/%-d")][field][tme] = ["", "", ""]

    # parse masterched
    f = open("mastersched.csv", "r")
    lines = f.readlines()
    for line in lines:
        c_fields = line.split(",")
        league = c_fields[0]
        dte = c_fields[1]
        tme = int(c_fields[2][0])
        if tme == 1: tme = 10
        t1 = c_fields[3]
        t2 = c_fields[4]
        field = int(c_fields[5][6:7])

        if dte in games.keys():
            games[dte][field][tme][0] = league
            games[dte][field][tme][1] = t1
            games[dte][field][tme][2] = t2

    # write to gsheet
    ssbull.update_acell('A1', sheet_date.strftime("%-m/%-d/%Y"))
    day_index = 1
    for dayinc in range(0,5):
        working_date = sheet_date + datetime.timedelta(days=dayinc)
        i = working_date.strftime("%a %-m/%-d")
        field_index = 3
        for field in [1, 2, 3, 4, 5]:
            time_index = 0
            day_field_values = []
            row = day_index + field_index
            for tme in [6, 7, 8, 10]:
                print("%9s  %2i  %i  %s %s  %s" %(i, tme, field, games[i][field][tme][0], games[i][field][tme][1], games[i][field][tme][2]))
                day_field_values.append(games[i][field][tme])
                time_index += 1

            #for x in range(0,len(day_field_values)):
            #    print(day_field_values[x])
            #print('D%i:F%i' % (row, row+3))

            ssbull.update('D%i:F%i' % (row, row+3), day_field_values)

            field_index += 5
        day_index += 30

