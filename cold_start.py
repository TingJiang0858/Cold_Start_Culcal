#!/usr/bin/python
import csv

dict = {}

# sturcture: dict{ owner{ application{ function{ trigger: [ [#cold_start] [clock] [#container]] }}}}

def readfile(rows, t):
    if dict.__contains__(rows[0]):
        if dict[rows[0]].__contains__(rows[1]):
            if dict[rows[0]][rows[1]].__contains__(rows[2]):
                if dict[rows[0]][rows[1]][rows[2]].__contains__(rows[3+t]):
                    return 1

                else:
                    dict[rows[0]][rows[1]][rows[2]][rows[3+t]] = []
            else:
                dict[rows[0]][rows[1]][rows[2]] = {rows[3+t]: []}
        else:
            dict[rows[0]][rows[1]] = {rows[2]: {rows[3+t]: []}}
    else:
        dict[rows[0]] = {rows[1]:{rows[2]:{rows[3+t]:[] } } }

    return 0

def cold_start_counting(flag, rows, invo,t):
    #print("2 ", dict[rows[0]][rows[1]][rows[2]][rows[3]][1])

    #int_invo = [int(x) for x in invo]                  # solve bug ' '
    int_invo = []
    for x in invo:
        try:
            int_invo.append(int(x))
        except:
            x = 0

    idle_time = 10
    cold_start = []
    count1 = []
    container1 = []

    if flag == 1 :
        cold = dict[rows[0]][rows[1]][rows[2]][rows[3+t]][0][0]
        count = dict[rows[0]][rows[1]][rows[2]][rows[3+t]][1][0]
        container = dict[rows[0]][rows[1]][rows[2]][rows[3+t]][2][0]
        #print(dict[rows[0]][rows[1]][rows[2]][rows[3]][2][0])
    else:
        cold = 0
        count = 1
        container = 0
        dict[rows[0]][rows[1]][rows[2]][rows[3+t]].append(cold_start)
        dict[rows[0]][rows[1]][rows[2]][rows[3+t]].append(count1)
        dict[rows[0]][rows[1]][rows[2]][rows[3+t]].append(container1)

    for invaction in int_invo:
        if count > idle_time:
            container = 0
        if invaction == 0:
            count += 1
        elif invaction > 0:
            count = 1
            if count <= idle_time and container < invaction:
                cold += (invaction - container)
                container = invaction
            if count > idle_time:
                cold += invaction
                container = invaction
        #print("cold, count, container", cold,count, container)
    cold_start.append(cold)
    count1.append(count)
    container1.append(container)

    dict[rows[0]][rows[1]][rows[2]][rows[3+t]][0] = cold_start
    dict[rows[0]][rows[1]][rows[2]][rows[3+t]][1] = count1
    dict[rows[0]][rows[1]][rows[2]][rows[3+t]][2] = container1

    #print("1 ", dict[rows[0]][rows[1]][rows[2]][rows[3]][2])
    #print("2", container1)

def main():

    j = 0
    for i in range(2):
        i += 1
        if i <= 3:
            filename = f'invocations_per_function_md.anon.d0{i}.csv'
            t = 1
        elif i <= 9:
            filename = f'invocations_per_function_md.anon.d0{i}.csv'
            t = 0
        else:
            filename = f'invocations_per_function_md.anon.d{i}.csv'
            t = 0
        with open(filename) as f:
            reader = csv.reader(f)
            title = next(reader)  # get first line
            for r in reader:
                flag = readfile(r, t)
                #print(flag, r)
                cold_start_counting(flag, r, r[4+t:],t)

    for each in dict.items():
        print(each)
'''
    filename = 'test.csv'
    t = 1
    # filename = 'test2.csv'
    with open(filename) as f:
        reader = csv.reader(f)
        title = next(reader)  # get first line
        for r in reader:
            flag = readfile(r, t)
            print(flag, r)
            cold_start_counting(flag, r, r[4 + t:], t)
'''

if __name__ == '__main__':
    main()
