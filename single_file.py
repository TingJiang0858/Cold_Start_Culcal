#!/usr/bin/python
import csv

dict = {}  # all of the owner
#owner = {}  # app
#app = {}  # function
#func = {}  # tri

def readfile(rows):

    #print(rows)

    if dict.__contains__(rows[0]):
        if dict[rows[0]].__contains__(rows[1]):
            if dict[rows[0]][rows[1]].__contains__(rows[2]):
                if dict[rows[0]][rows[1]][rows[2]].__contains__(rows[3]):
                    i = 1  # !!!!!!!!!!!!!!!!!!!!!

                else:
                    dict[rows[0]][rows[1]][rows[2]][rows[3]] = []
            else:
                dict[rows[0]][rows[1]][rows[2]] = {rows[3]: []}

        else:
            dict[rows[0]][rows[1]] = {rows[2]: {rows[3]: []}}
    else:
        dict[rows[0]] = {rows[1]:{rows[2]:{rows[3]:[] } } }
        #owner[rows[1]] = app
        #app[rows[2]] = func
        #func[rows[3]] = [rows[4:],[]]

    #print("dict = ", dict)

def cold_start_counting(rows, invo):
    int_invo = [int(x) for x in invo]
    #print(int_invo)
    idle_time = 10
    cold_start = []
    cold = 0
    count = 0
    container = 0
    clock = 0
    for invaction in int_invo:
        #print("invaction = ", invaction)
        clock += 1
        if count > idle_time:
            container = 0
        if invaction == 0:
            count += 1
        elif invaction > 0:
            count = 0
            if count <= idle_time and container < invaction:
                cold += (invaction - container)
                container = invaction
            if count > idle_time:
                cold += invaction
                container = invaction
        #print("cold, count, container", cold,count, container)    # transit clock!!!!!!!!!!!!
    cold_start.append(cold)
    #print("cold_start = ", cold_start)
    dict[rows[0]][rows[1]][rows[2]][rows[3]].append(cold_start)
    # print(dict)


def main():
    rows = []
    filename = 'test2.csv'
    with open(filename) as f:
        reader = csv.reader(f)
        title = next(reader)  # get first line
        for r in reader:
            #print("r",r)
        #rows = next(reader)
            readfile(r)                                         #!!!!!!!
            cold_start_counting(r, r[4:])

    print(dict)
if __name__ == '__main__':
    main()
    # print(__name__)
