import win32com.client
import os, h5py, numpy
import xml.etree.ElementTree as ET
from support import sc3_LoadPrb,sc3_SaveRes

# loading samples
pnames,sampA,sampB,sampC,sampD =        \
sc3_LoadPrb('test_sedi','samples','samples.txt')

# init HEC-RAS Controller
hec = win32com.client.Dispatch('RAS505.HECRASController')
projekt = os.path.join(os.getcwd(),r'test_sedi\test_sedi.prj')  # project name
hec.ShowRas()                                           # show HEC-RAS window
# loading River Stations from geometry
hdfname = os.path.join(os.getcwd(),r'test_sedi\test_sedi.g03.hdf')
dane = h5py.File(hdfname,'r')                   # opening of HDF file
# link to the River Stations in HDF file
ListRS = dane.get('Geometry').get('Cross Sections').get('River Stations')
GeomRS = numpy.empty([len(ListRS)],dtype='S15')     # NumPy array of RSes
for i in range(0,len(ListRS)):
    GeomRS[i] = ListRS[i]
dane.close()
NXS = len(GeomRS)               # number of cross-sections

# test of loaded samples
sname = os.path.join(os.getcwd(),r'test_sedi\test_sedi.s01')
ii = 0
for sample in [sampA, sampB, sampC, sampD]:
    plik = ET.parse(sname)  # opening XML file with sediment data
    dane = plik.getroot()   # access to bed gradations
    grad = dane.find('Bed_Gradation').find('Sample').find('Gradation')
    for elm in sample:      # assignment of tested sample
        grad.attrib[elm] = sample[elm]
    plik.write(os.path.join(os.getcwd(),r'test_sedi\test_sedi.s01'))
    del plik
    hec.Project_Open(projekt)                   # open HEC-RAS project
    test1 = hec.Plan_SetCurrent('plan sedi00')  # setting sediment plan
    NMsg,TabMsg,block = None,None,True  # no. and list of messages, blocking
    # computations of the current plan
    v1,NMsg,TabMsg,v2 = hec.Compute_CurrentPlan(NMsg,TabMsg,block)
    del NMsg, TabMsg, block
    hec.Project_Close()             # close HEC-RAS project
    # full path to the HDF file results of the computations
    hdfname = os.path.join(os.getcwd(),r'test_sedi\test_sedi.p03.hdf')
    dane = h5py.File(hdfname,'r')   # opening of HDF file
    # accessing bed elevations
    XSbed = dane.get('Results').get('Sediment').get('Output Blocks')
    XSbed = XSbed.get('Sediment').get('Sediment Time Series')
    XSbed = XSbed.get('Cross Sections').get('Invert Elevation')
    NTS = len(XSbed)
    # accessing WSE
    XSwse = dane.get('Results').get('Sediment').get('Output Blocks')
    XSwse = XSwse.get('Sediment').get('Sediment Time Series')
    XSwse = XSwse.get('Cross Sections').get('Water Surface')
    # NumPy arrays for bed elevations and WSE
    InitBed = numpy.empty([NXS],dtype=float)    # initial bed and WSE
    InitWSE = numpy.empty([NXS],dtype=float)
    LastBed = numpy.empty([NXS],dtype=float)    # final bed and WSE
    LastWSE = numpy.empty([NXS],dtype=float)
    for i in range(0,NXS):          # assigment of bed and WSE form HDF
        InitBed[i] = XSbed[0][i]    # to NumPy arraya
        InitWSE[i] = XSwse[0][i]
        LastBed[i] = XSbed[NTS-1][i]
        LastWSE[i] = XSwse[NTS-1][i]
    dane.close()
    del dane
    sc3_SaveRes(pnames[ii],sample,GeomRS,InitBed,InitWSE,LastBed,LastWSE)
    ii += 1

hec.QuitRas()       # close HEC-RAS
del hec             # delete HEC-RAS controller