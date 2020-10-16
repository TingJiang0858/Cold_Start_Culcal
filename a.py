#!/usr/bin/env python3
import csv
import sys, getopt
import os
import time
from pprint import pprint


# global variables
owner = {}
invo_time = None

def managing_owner_dict (hashowner, hashapp, hashfunction, trigger):
    global owner
    if hashowner not in owner:
        owner[hashowner] = {}
        owner[hashowner][hashapp] = {}
        owner[hashowner][hashapp][hashfunction] = {}
        owner[hashowner][hashapp][hashfunction][trigger] = {}
        owner[hashowner][hashapp][hashfunction][trigger]["cnt_invocation"] = 0
        owner[hashowner][hashapp][hashfunction][trigger]["cnt_coldstarts"] = 0
        owner[hashowner][hashapp][hashfunction][trigger]["freq_coldstarts"] = {}
        owner[hashowner][hashapp][hashfunction][trigger]["containers"] = {}

    else:
        # owner is in the owner dict
        if hashapp not in owner[hashowner]:
            owner[hashowner][hashapp] = {}
            owner[hashowner][hashapp][hashfunction] = {}
            owner[hashowner][hashapp][hashfunction][trigger] = {}
            owner[hashowner][hashapp][hashfunction][trigger]["cnt_invocation"] = 0
            owner[hashowner][hashapp][hashfunction][trigger]["cnt_coldstarts"] = 0
            owner[hashowner][hashapp][hashfunction][trigger]["freq_coldstarts"] = {}
            owner[hashowner][hashapp][hashfunction][trigger]["containers"] = {}

        else:
            if hashfunction not in owner[hashowner][hashapp]:
                owner[hashowner][hashapp][hashfunction] = {}
                owner[hashowner][hashapp][hashfunction][trigger] = {}
                owner[hashowner][hashapp][hashfunction][trigger]["cnt_invocation"] = 0
                owner[hashowner][hashapp][hashfunction][trigger]["cnt_coldstarts"] = 0
                owner[hashowner][hashapp][hashfunction][trigger]["freq_coldstarts"] = {}
                owner[hashowner][hashapp][hashfunction][trigger]["containers"] = {}
            else:

                if trigger not in owner[hashowner][hashapp][hashfunction]:
                    owner[hashowner][hashapp][hashfunction][trigger] = {}
                    owner[hashowner][hashapp][hashfunction][trigger]["cnt_invocation"] = 0
                    owner[hashowner][hashapp][hashfunction][trigger]["cnt_coldstarts"] = 0
                    owner[hashowner][hashapp][hashfunction][trigger]["freq_coldstarts"] = {}
                    owner[hashowner][hashapp][hashfunction][trigger]["containers"] = {}
                else:
                    # do nothing
                    pass
    return

# main function
def main(argv):

    global owner
    global invo_time

    max_idle = int(argv[0])

    maindir = './output_sep'
    if not os.path.exists(maindir):
        os.makedirs(maindir)

    subdir = maindir + "/result_with_" + str(max_idle)
    if not os.path.exists(subdir):
        os.makedirs(subdir)

    result_csv = subdir + '/result_cold_start_id' + str(max_idle)+ '.csv'

    for day in range(1, 15):

        # time.sleep(1)
        fname = "./az_data/invocations_per_function_md.anon.d" + \
            ("%02d" % day) + ".csv"

        print ("Day:", day, fname)

        with open(fname) as csvfile:

            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                if row[0] == "HashOwner":
                    continue

                invo_time = (day - 1) * 1440 + 1

                invo = {}
                hashowner = row[0]
                hashapp = row[1]
                hashfunction = row[2]
                trigger = row[3]

                managing_owner_dict (hashowner, hashapp, hashfunction, trigger)
                for str_invo_cnt in row[4:]:
                    invo_cnt = int(str_invo_cnt)
                    func = owner[hashowner][hashapp][hashfunction][trigger]

                    # create containers and cold starts...
                    if invo_cnt > 0:
                        func["cnt_invocation"] = func.get("cnt_invocation", 0) + invo_cnt
                        remain_cnt = invo_cnt
                        for k,v in func["containers"].items():
                            func["containers"][k]["time_last_exec"] = invo_time
                            remain_cnt = remain_cnt - 1
                            if remain_cnt == 0:
                                break

                        if remain_cnt > 0:
                            # create new container to this function
                            if len(func["containers"]) == 0:
                                nc_key = 0
                            else:
                                nc_key = max(func["containers"], key=int) + 1

                            for _ in range(remain_cnt):
                                if nc_key in func["containers"]:
                                    print ("Error: Duplicated Container ID: %d" % nc_key)
                                    sys.exit()

                                func["containers"][nc_key] = {}
                                func["containers"][nc_key]["time_created"] = invo_time
                                func["containers"][nc_key]["time_last_exec"] = invo_time

                                # update cold_start cnt
                                func["cnt_coldstarts"] = func.get("cnt_coldstarts", 0) + 1

                                # key increase
                                nc_key = nc_key + 1

                    # cleanup containers
                    del_keys = []
                    for k,v in func["containers"].items():
                        if abs(invo_time - int(func["containers"][k]["time_last_exec"])) >= max_idle:
                            del_keys.append(k)

                    # delete container
                    for dk in del_keys:
                        del func["containers"][dk]

                    invo_time += 1

    total_in = 0
    total_cs = 0

    # below are for double-check
    tot_in2 = 0
    tot_cs2 = 0

    with open(result_csv, mode='w') as csv_file:
        w = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['Owner', 'App', 'Func', 'Tri', 'Coldstart', 'Total Invocation', "CS Ratio"])

        for key, value in owner.items():
            tot_in_owner = 0
            tot_cs_owner = 0
            for appk, appv in value.items():
                tot_in_app = 0
                tot_cs_app = 0
                for funk, funv in appv.items():
                    for trigk, trigv in funv.items():
                        trigger = trigk
                        ratio = round(trigv["cnt_coldstarts"]/trigv["cnt_invocation"], 6)

                        w.writerow([key, appk, funk, trigger, trigv["cnt_coldstarts"], trigv["cnt_invocation"], ratio])
                        tot_in_app += trigv["cnt_invocation"]
                        tot_cs_app += trigv["cnt_coldstarts"]

                        tot_in2 += trigv["cnt_invocation"]
                        tot_cs2 += trigv["cnt_coldstarts"]

                tot_in_owner += tot_in_app
                tot_cs_owner += tot_cs_app

            total_in += tot_in_owner
            total_cs += tot_cs_owner

    print ("Total statistics:", total_cs, ",", total_in, ", Ratio:", round(total_cs/total_in, 6)*100, "%")
    print ("Total statistics:", tot_cs2, ",", tot_in2, ", Ratio:", round(tot_cs2/tot_in2, 6)*100, "%")

if __name__ == "__main__":
    main(sys.argv[1:])
