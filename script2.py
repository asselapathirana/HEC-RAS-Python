import win32com.client, os, math
import numpy as np
from scipy import optimize as opt
from support import sc2_ReadObs

def ObjFun(x):                  # objective function
    global hec,RivID,RchID,WSE_ID,ProfID,RivName,RchName,nRS,RScmp,RStyp
    global Nobs,iRSobs,WSEobs
    nLOB,nCh,nROB = x[0],x[1],x[2]
    for i in range(0,nRS):
        ErrMsg   = None     # list of error messages
        v0,v1,v2,v3,v4,v5,v0,ErrMsg =                   \
        hec.Geometry_SetMann_LChR(RivName,RchName,RScmp[i],nLOB,nCh,nROB,ErrMsg)
    NMsg,ListMsg,block = None,None,True     # no. and list of messages, blocking
    v1,NMsg,ListMsg,v2 = hec.Compute_CurrentPlan(NMsg,ListMsg,block)
    TotSum = 0.0        # total sum of square errors
    for i in range(0,Nobs):
        wse,v1,v2,v3,v4,v5,v6 =                         \
        hec.Output_NodeOutput(RivID,RchID,iRSobs[i],100,ProfID,WSE_ID)
        TotSum += (wse - WSEobs[i])**2      # single square error added
    TotSum = math.sqrt( TotSum / Nobs )     # final value
    return TotSum

def PokazIter(xk):              # iteration control function
    print(('nLOB=%15.6f, nCh=%15.6f, nROB=%15.6f, ' %        \
    (xk[0],xk[1],xk[2])))
    print(('   funk=%15.6f' % (ObjFun(xk))))
    return 0

# observed: number, RSes as strings, RSes as floats, WSEs
Nobs,lRSobs,dRSobs,WSEobs = sc2_ReadObs('test01','ObsH','ObsH1x.txt')
# init HEC-RAS Controller
hec = win32com.client.Dispatch('RAS505.HECRASController')
RivID,RchID = 1,1    # ID of river and reach
ProfID,WSE_ID = 1,2  # ID of profile, ID of WSE variable
projekt = os.path.join(os.getcwd(),r'test01\test01.prj')    # project file
hec.Project_Open(projekt)               # opening HEC-RAS
hec.ShowRas()                           # show HEC-RAS window
# setting current computational plan
test1 = hec.Plan_SetCurrent('plan_basic')
# river and reach names
RivName,RchName = 'Warta','Dop_Jeziorsko'
# number and list of messages, blocking mode
NMsg,TabMsg,block = None,None,True
# computations of the current plan
v1,NMsg,TabMsg,test2 = hec.Compute_CurrentPlan(NMsg,TabMsg,block)
# numbers of nodes with observations
iRSobs = np.empty([Nobs],dtype=int)
for i in range(0,Nobs):
    iRSobs[i],v1,v2,v3 = hec.Output_GetNode(RivID,RchID,lRSobs[i])
# computational: number, RS and types
nRS,RScmp,RStyp = None,None,None
v1,v2,nRS,RScmp,RStyp = hec.Output_GetNodes(RivID,RchID,nRS,RScmp,RStyp)

print ("\nIteration process: Nealder-Mead simplex")
x0 = np.array([0.08,0.014,0.08])                # initial solution
Xopt = opt.fmin(ObjFun,x0,callback=PokazIter)   # optimization

hec.QuitRas()       # close HEC-RAS
del hec             # delete HEC-RAS controller
