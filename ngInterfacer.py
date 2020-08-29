import os
import numpy as np
import re
import pandas as pd
import matplotlib.pyplot as plt

class data:
    def __init__(self, fname='./data.dat'):
        """
        This is a class that reads back the data from the simulator.
        fname       string      filename path to read

        This class, after the the extract() method is ran, returns saves in the class, index, x and y.
        To generate example data run !ngspice -b xspice_c1.cir > test.dat
        """
        self.path = fname
        datatemp = []
        with open(fname, 'r') as fin:
            datatemp=fin.readlines()
        self.data = datatemp

    def extract(self):
        temp = [re.findall('\d+\t', n) for n in self.data]
        extrData =  [self.data[index] for index, n in enumerate(temp) if n!=[]]
        index =  [float(n.strip().split('\t')[0]) for n in extrData]
        x =  [float(n.strip().split('\t')[1]) for n in extrData]
        y =  [float(n.strip().split('\t')[2]) for n in extrData]
        self.index = index 
        self.x = x 
        self.y = y

class circuit:
    def __init__(self, fname='./xspice_c1.cir'):
        """
        This is a class tha reads the circuit netlist and manipulates it
        """
        self.path = fname
        with open(fname, 'r') as fin:
            netlistemp=fin.readlines()
        self.netlist = netlistemp

    def typeSet(self, stringNumberInput):
        """
        This method typesets numbers like so: 100k = 100e3; 1.2n = 1.2e-9
        """

    def getInstanceVal(self, instance=''):
        """
        This method gets the value of an instance.
        ... Requires work, use the typeset value above to rename: p, n, u, k and M to 1e-12, ... etc.
        """
        if instance=='':
            print('Empty instance signifier - skipping')
        else:
            tempVar = [(ind,n) for ind,n in enumerate(self.netlist) if re.findall(instance, n)]
            if not tempVar:
                print('Instance not found')
            elif len(tempVar)>1:
                print('Multiple instances found, please be more specific:')
                print(tempVar)
            else:
                if re.findall('^[rlc]', tempVar[0][1]):
                    # If passive element return the value
                    value = tempVar[0][1].split('\n')[0].split(' ')[-1]
                    return value
                else:
                    print('not a passive R, L or C element')
                    return tempVar

    def getln(self, regexp='^\.'):
        """
        In this method the line number where regexp is returned
        netlist     list    The netlist list read in the init above
        regexp      string  The expression of interest
        Usage:
            nlst = circuit()
            nlst.getln('vin')
        """
        tempVar = [(ind,n) for ind,n in enumerate(self.netlist) if re.findall(regexp, n)]
        return tempVar

    def replaceStrPat(self, existingPattern, patternToReplace, stringToManipulate):
        """
        This method replaces part of a string in a netlist line from getln above
        existingPattern     string  The pattern present in the string
        patternToReplace    string  The pattern you wish to replacne
        stringToManipulate  string  The string that will be replaced
        Usage:
            nlst = circuit()
            testPattern = nlst.getln('vin')[0][1]
            nlst.replaceln('vin 1', 'vin 1.23', testPattern)
        """
        tempString = re.sub(existingPattern,patternToReplace, stringToManipulate)
        return tempString

    def runSim(self, dataPath='./data.dat'):
        """
        This method simulates the netlist saved in netlistPath and exports the data saved in dataPath
        dataPath        string  Path and file name where the .dat file will be saved
        """
        if dataPath=='':
            print('Not a valid .dat filename or path. for example please use: \'./data.dat\'')
        else:
            os.system('ngspice -b '+self.path+' > '+dataPath)
            return print('done')



nlst = circuit()
nlst.getInstanceVal('rbias1')

#asd = !ngspice -b xspice_c1.cir > data.dat
#sim = data()
#sim.extract()
