import win32com.client
import os, numpy
from support import sc1_ShowNodes

# Initiate the RAS Controller class
hec = win32com.client.Dispatch("RAS505.HECRASController")
hec.ShowRas()                       # show HEC-RAS window
# full filename of the RAS project
RASProject = os.path.join(os.getcwd(),r'test01\test01.prj')
hec.Project_Open(RASProject)        # opening HEC-RAS
# to be populated: number and list of messages, blocking mode
NMsg,TabMsg,block = None,None,True
# computations of the current plan
v1,NMsg,TabMsg,v2 = hec.Compute_CurrentPlan(NMsg,TabMsg,block)
# ID numbers of the river and the reach
RivID,RchID = 1,1
# to be populated: number of nodes, list of RS and node types
NNod,TabRS,TabNTyp = None,None,None
# reading project nodes: cross-sections, bridges, culverts, etc.
v1,v2,NNod,TabRS,TabNTyp =                      \
hec.Geometry_GetNodes(RivID,RchID,NNod,TabRS,TabNTyp)
# ID of output variables: WSE, ave velocity
WSE_id,AvVel_id = 2,23
TabWSE = numpy.empty([NNod],dtype=float)    # NumPy array for WSE
TabVel = numpy.empty([NNod],dtype=float)    # NumPy array for velocities
for i in range(0,NNod):         # reading over nodes
    if TabNTyp[i] == "":        # simple cross-section
        # reading single water surface elevation
        TabWSE[i],v1,v2,v3,v4,v5,v6 =           \
        hec.Output_NodeOutput(RivID,RchID,i+1,0,1,WSE_id)
        # reading single velocity
        TabVel[i],v1,v2,v3,v4,v5,v6 =           \
        hec.Output_NodeOutput(RivID,RchID,i+1,0,1,AvVel_id)
hec.QuitRas()       # close HEC-RAS
del hec             # delete HEC-RAS controller

sc1_ShowNodes( NNod, TabRS, TabNTyp, TabWSE, TabVel )
