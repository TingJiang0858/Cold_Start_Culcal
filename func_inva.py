#!/usr/bin/python
import csv

dict = {}  # all of the owner
owner = {}  # app
app = {}  # function
func = {}  # tri

def readfile(rows):

    #print(rows)

    if dict.__contains__(rows[0]):
        if owner.__contains__(rows[1]):
            if app.__contains__(rows[2]):
                if func.__contains__(rows[3]):
                    i = 1  # !!!!!!!!!!!!!!!!!!!!!

                else:
                    func[rows[3]] = rows[4:]
            else:
                app[rows[2]] = func
                func[rows[3]] = rows[4:]
        else:
            owner[rows[1]] = app
            app[rows[2]] = func
            func[rows[3]] = rows[4:]
    else:
        dict[rows[0]] = owner
        owner[rows[1]] = app
        app[rows[2]] = func
        func[rows[3]] = [rows[4:],[]]

    print("dict = ", dict)


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
        print("invaction = ", invaction)
        clock += 1
        if count > idle_time:
            container = 0

        if invaction == 0:
            count +=1
        elif invaction > 0:
            if count <= idle_time and container < invaction:
                cold += (invaction - container)
                count = 0
                container = invaction
            if count > idle_time:
                cold += invaction
                count = 0
                container = invaction
        print("cold, count, container", cold,count, container,clock)    # transit clock!!!!!!!!!!!!
    cold_start.append(cold)
    func[rows[3]][1] = cold_start
    print(dict)


def main():
    rows = []
    filename = 'test1.csv'
    with open(filename) as f:
        reader = csv.reader(f)
        title = next(reader)  # get first line
        #for r in reader:
        rows = next(reader)
        readfile(rows)                                         #!!!!!!!
        cold_start_counting(rows, rows[4:])

if __name__ == '__main__':
    main()
    # print(__name__)
