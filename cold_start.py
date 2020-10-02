#!/usr/bin/python
import csv
import datetime
import math

dict = {}
total = 0
totalc = 0
#total_trigger ={'http':0,'queue':0,'event':0,'orchestration':0,'timer':0,'storage':0,'others':0}

# sturcture: dict{ owner{ application{ function{ trigger: [ [#cold_start] [#container] [file]] }}}}

def readfile(rows):
    if dict.__contains__(rows[0]):
        if dict[rows[0]].__contains__(rows[1]):
            if dict[rows[0]][rows[1]].__contains__(rows[2]):
                if dict[rows[0]][rows[1]][rows[2]].__contains__(rows[3]):
                    return 1

                else:
                    dict[rows[0]][rows[1]][rows[2]][rows[3]] = []
            else:
                dict[rows[0]][rows[1]][rows[2]] = {rows[3]: []}
        else:
            dict[rows[0]][rows[1]] = {rows[2]: {rows[3]: []}}
    else:
        dict[rows[0]] = {rows[1]:{rows[2]:{rows[3]:[] } } }

    return 0

def cold_start_counting(flag, rows, invo,f):
    #print("2 ", dict[rows[0]][rows[1]][rows[2]][rows[3]][1])

    #int_invo = [int(x) for x in invo]                  # solve bug ' '
    global totalc
    global total

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
        cold = dict[rows[0]][rows[1]][rows[2]][rows[3]][0][0]
        container = dict[rows[0]][rows[1]][rows[2]][rows[3]][1]
        file = dict[rows[0]][rows[1]][rows[2]][rows[3]][2]
    else:
        cold = 0
        container = []
        file = f
        dict[rows[0]][rows[1]][rows[2]][rows[3]].append(cold_start)
        dict[rows[0]][rows[1]][rows[2]][rows[3]].append(container1)
        dict[rows[0]][rows[1]][rows[2]][rows[3]].append(file)
    cold1 = 0
    if f > int(file + 1):
        container = []

    for invaction in int_invo:
        #print("ca", container)
        total += invaction
        #total_trigger[rows[3]] += invaction
        contain_total = 0
        temp = 1
        if container:
            for i in range(len(container)):
                if i +1 >= len(container):
                    break
                elif container[i][1] == container[i+1][1]:
                    container[i][0] += container[i+1][0]
                    container.pop(i+1)
            for list1 in container:             # all clock + 1
                list1[1] += 1
                contain_total += list1[0]
            for list1 in container:
                if list1[1] > idle_time:
                    container.remove(list1)
            for list1 in container:
                if math.fabs(list1[0]) == 0:
                    container.remove(list1)
        if invaction == 0:
            continue
        if invaction > 0:
            if contain_total <= invaction:
                cold1 += (invaction - contain_total)
                container = []
                list2 =[]
                list2.append(invaction)
                list2.append(1)
                container.append(list2)
            elif contain_total > invaction:
                tem = invaction
                for list3 in container:
                    temp = tem - list3[0]
                    if temp > 0:
                        tem -= list3[0]
                        list4 = [list3[0],1]
                        list3[0] = 0
                        container.append(list4)
                        continue
                    elif temp <= 0:
                        container.append([(list3[0] + temp),1])
                        list3[0] = int(math.fabs(temp))
                        break
    totalc += cold1
    cold2 = cold + cold1
    cold_start.append(cold2)

    dict[rows[0]][rows[1]][rows[2]][rows[3]][0] = cold_start
    dict[rows[0]][rows[1]][rows[2]][rows[3]][2] = f
    dict[rows[0]][rows[1]][rows[2]][rows[3]][1] = container

def main():
    start = datetime.datetime.now()
    #print("start time ", start)
    #print("input idle time:")
    #idle = sys.argv[1]
    j = 0
    for i in range(14):
        i += 1
        if i <= 9:
            filename = f'invocations_per_function_md.anon.d0{i}.csv'
        else:
            filename = f'invocations_per_function_md.anon.d{i}.csv'
        with open(filename) as f:
            #print("filename: ", filename)
            reader = csv.reader(f)
            title = next(reader)  # get first line
            for r in reader:
                flag = readfile(r)
                #print(i,r)
                cold_start_counting(flag, r, r[4:],i)
#    for each in dict.items():
#        print(each)
    end = datetime.datetime.now()
    #print("time = ", end - start )
    print(total, totalc)
    #print(total_trigger)
    #print(dict)


if __name__ == '__main__':
    main()
