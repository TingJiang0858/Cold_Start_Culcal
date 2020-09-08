import csv

class Func_invo:
    def __init__(self,owner, app, func, tri, inv):
        self.owner = owner
        self.app = app
        self.func = func
        self.tri = tri
        self.inv = inv

    def cold_culcal(self,cold_start):
        self.cold_start = cold_start
        
  #  def p(self):
  #      print(self.inv)

rows = []
filename = 'test1.csv'
with open(filename) as f:
    reader = csv.reader(f)
    title = next(reader)        # get first line
    for r in reader:
        rows.append(r)

#print(rows)
r = []
obj = []
i = 0
for row in rows:
    r = row
#    print(r)
    del r[0:4]
    temp = Func_invo(row[0],row[1],row[2],row[3],r)
    #print(r)
    obj.append(temp)
    #print(obj)

idle_time = 10
start = []
for i in range(len(rows)):
    print(obj[i].inv)
    cold = 0
    count = 0
    for invaction in obj[i].inv:
        #print(invaction)
        if int(invaction) == 0:
            count +=1
        if int(invaction) == 1 and count <= idle_time:
            count = 0
        if int(invaction) == 1 and count > idle_time:
            cold +=1
            count = 0
    start.append(cold)
print(start)





