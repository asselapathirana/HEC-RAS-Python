import os
import numpy as np

def MakePath(*args):
    ''' linking elements of list args into one path '''
    fpath = os.getcwd()
    for item in args:
        fpath = os.path.join(fpath,item)
    return fpath

def sc1_ShowNodes(NRS,ListRS,ListTyp,ResWSE,ResVel):
    print(("\nNumber of nodes: %10d" % (NRS)))
    print(("%10s %15s %15s %15s %15s" %                  \
    ('no.', 'RS', 'type', "WSE", "Vel")))
    for i in range(0,NRS):
        if ListTyp[i] == "":
            print(("%10d %15s %15s %15.2f %15.2f" %      \
            (i+1,ListRS[i],ListTyp[i],ResWSE[i],ResVel[i])))
        else:
            print(("%10d %15s %15s" % (i+1,ListRS[i],ListTyp[i])))
    print ("")
    return 0

def sc2_ReadObs(projdir,obsdir,obsfile):
    ''' reading of observed water surface elevations
        projdir - project directory
        obsdir  - directory with observed data inside 'projdir'
        obsfile - file with observed data inside 'obsdir'
        results: Nobs   - number of observed data
                 lRSobs - NumPy array of RS as strings
                 dRSobs - NumPy array of RS as float numbers
                 WSEobs - NumPy array of WSE as float numbers '''
    # number of observed data, list of observed RS, list of observed WSE
    Nobs,ListRS,ListWSE  = 0,[],[]
    # full path to the file with observed WSE
    fname = MakePath(projdir,obsdir,obsfile)
    plik = open(fname,'r')
    licz = 0        # counter of lines in file
    # reading of observed data
    for line in plik.readlines():
        if licz!=0:
            lista = line.split()
            ListRS.append(lista[0])
            ListWSE.append(lista[1])
            Nobs += 1
        licz+=1
    plik.close()
    # NumPy arrays: RS as strings, RS as float, WSE as float
    lRSobs = np.empty([Nobs],dtype='S15')
    dRSobs  = np.empty([Nobs],dtype=float)
    WSEobs = np.empty([Nobs],dtype=float)
    for i in range(0,Nobs):
        lRSobs[i] = ListRS[i]
        dRSobs[i] = float(ListRS[i])
        WSEobs[i] = float(ListWSE[i])
    return Nobs, lRSobs, dRSobs, WSEobs

def sc3_LoadPrb(projdir,prbdir,prbfile):
    ''' sample of sediments for tests
        projdir - project director
        prbdir  - directory with sediment samples, inside projdir
        prbfile - file with sediment samples, inside prbdir
        results: prbname - names of samples
                 prbA,prbB,prbC,prbD - dictonary with bed gradations  '''
    # full path to the tested sediment samples
    sname = MakePath(projdir,prbdir,prbfile)
    plik = open(sname,'r')
    i = 0
    prbname = []    # list of sample names
    prbA,prbB,prbC,prbD  = {},{},{},{}
    for linia in plik.readlines():
        lista = linia.split()
        if i > 0:
            prbA[lista[5]] = lista[6]
            prbB[lista[5]] = lista[7]
            prbC[lista[5]] = lista[8]
            prbD[lista[5]] = lista[9]
        else:
            prbname.append(lista[6])
            prbname.append(lista[7])
            prbname.append(lista[8])
            prbname.append(lista[9])
        i += 1
    plik.close()
    return prbname, prbA, prbB, prbC, prbD

def sc3_SaveRes(fname,sample,ListRS,InitBed,InitWSE,LastBed,LastWSE):
    ''' saving of results obtained from sinlge simulation
        fname - results file
        sample - dictonary of sample
        ListRS  - NumPy array of RS as  of strings
        InitBed - NumPy array of initial bed elevations
        InitWSE - NumPy array of initial WSE
        LastBed - NumPy array of final bed elevations
        LastWSE - NumPy array of final WSE                    '''
    def SortClasses(sample):
        ''' list for sorted access to sample classes
            sample - sorting of classes for selected sample
            result: list - sorted list of class numbers       '''
        lista0 = list(sample.keys())
        lista = []
        for klasa in lista0:
            lista.append(int(klasa[2:]))
        lista.sort()
        return lista
    klasy = SortClasses(sample)     # sediment classes
    plik = open(fname+".txt",'w')   # opening results file
    plik.write('sample\n')          # writing sample
    plik.write("%10s %15s\n"%("class","fraction"))
    for klasa in klasy:
        kl = 'GC' + str(klasa)
        plik.write("%10s %15.2f\n"%(kl,float(sample[kl])))
    plik.write('\nresults\n')       # writing results
    plik.write("%10s %15s %15s %15s %15s %15s\n"%               \
    ("no","RS","InitBed","InitWSE","LastBed","LastWSE"))
    for i in range(0,len(ListRS)):
        plik.write("%10d %15s %15.2f %15.2f %15.2f %15.2f\n"%   \
        (i,ListRS[i],InitBed[i],InitWSE[i],LastBed[i],LastWSE[i]))
    plik.close()
    return 0