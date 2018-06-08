__author__ = 'grizzly'

import sys
import random

simulation_error = """
            Error of simulation
Check the entered data. It must look like:
   ./simulate.py -n 10 --random
OR
   ./simulate.py -n 6 --mirror
  where '-n' - note for  number of server,
  '6' - number of severs,it must be even number
  '--random' OR '--mirror' - method of simulation
"""

class Simulator:
    servers_number = None
    method = None
    data = ()

    def __init__(self,servers_number,method):
        self.servers_number = servers_number
        self.method = method

    def start(self):
        i = 1
        fragments = tuple( i for i in range(1,int(5*self.servers_number/2 + 1)))
        if self.method == '--mirror':
            self.data = self.mirrored(fragments)
        else:
            self.data = self.randomed(fragments)
        lost_data = 0
        for i in range(servers_number):
            lost_elements = 0
            for j in range(servers_number):
                if i < j and len(set(self.data[i])&set(self.data[j]))>0:
                    lost_elements += 1
                    #print("Losted el num "+str(len(set(self.data[i])&set(self.data[j]))))
                    #print(self.data[i])
                    #print(self.data[j])
            lost_data= max(lost_data,lost_elements)
        probability = lost_data/(servers_number-1) * 100
        #print(lost_data)
        print ('Killing 2 arbitrary servers results in data loss in '+str(probability)+'% cases')

    def mirrored(self,fragments):
        self.data =tuple(fragments[5*i:5*(i+1)] for i in range(0,int(servers_number/2)))*2
        return self.data

    def randomed(self,fragments):
        self.data = tuple([] for i in range(servers_number))
        for k in range(len(fragments)):
            #print('Fragment='+str(fragments[k]))
            if int(fragments[k]) != len(fragments):
                for j in range(2):
                    added = False
                    while  added == False:
                        i = random.randint(0,servers_number-1)
                        #print(i)
                        if (len(self.data[i])) < 5 and (self.data[i].count(fragments[k])==0):
                            self.data[i].append(fragments[k])
                            added = True
            else:
                count_of_frag = list(len(self.data[i]) for i in range(servers_number))
                if count_of_frag.count(3) == 1:
                    bad_server = count_of_frag.index(3)
                    for i in range(servers_number):
                        if i != bad_server and len(set(self.data[bad_server])&set(self.data[i]))==0:
                            self.data[bad_server].append(self.data[i][0])
                            self.data[bad_server].append(fragments[k])
                            self.data[i].pop(0)
                            self.data[i].append(fragments[k])
                            break
                else:
                    for j in range(2):
                        added = False
                        while  added == False:
                            i = random.randint(0,servers_number-1)
                            if (len(self.data[i])) < 5 and (self.data[i].count(fragments[k])==0):
                                self.data[i].append(fragments[k])
                                added = True
                                #print(self.data)
        return self.data

if __name__== "__main__":
    if len(sys.argv) != 4:
        print (simulation_error)
        #print ('A')
    else:
        n = sys.argv[1]
        method = sys.argv[3]
        try:
            servers_number = int(sys.argv[2])
        except ValueError:
            print (simulation_error)
            #print ('B')
        else:
            if n !='-n' or (method !='--random' and method != '--mirror') or servers_number < 2 or servers_number%2 !=  0 :
                print (simulation_error)
                #print ('C')
            else:
                simulation = Simulator(servers_number,method)
                simulation.start()
