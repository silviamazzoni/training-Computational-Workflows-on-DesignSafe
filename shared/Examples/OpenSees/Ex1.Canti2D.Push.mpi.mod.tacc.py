# mpiexec -np 3 python Ex1a.Canti2D.Push.mpi.tacc.py
# pip install OpenSeesPy

# import openseespy.opensees as ops

# # import sys
# # OpenSeesPyPath = r'/opt/apps/intel24/impi21/opensees/3.7.1/bin' 
# # sys.path.append(OpenSeesPyPath) 
# # # import opensees as ops 


import numpy as numpy
import matplotlib.pyplot as plt
import sys
import os

# Import the local version of OpenSees, if it exists
if os.path.exists('opensees.so'):
    import opensees as ops;
else:
    import openseespy.opensees as ops

ops.start()
pid = ops.getPID()
np = ops.getNP()
print(f'pid {pid} of {np} started')

if len(sys.argv)>1:
    print(f'mpi -- python pid {pid} of {np} Command-Line Arguments (argv): {sys.argv}')

LColList = [100,120,200,240,300,360,400,480]
LColList = [100,120]
#-----------------------------------------
dataDir=f'DataPYmpi';                # set up name of data directory
os.makedirs(dataDir, exist_ok=True); # create data directory

count = 0;
for Lcol in LColList:
    # check if count is a multiple of pid : "is it its turn?"
    if count % np == pid:
        ops.wipe()
        
        # SET UP ----------------------------------------------------------------------------
        ops.wipe()     #  clear opensees model
        ops.model('basic','-ndm',2,'-ndf',3)     #  2 dimensions, 3 dof per node
        
        
        # define GEOMETRY -------------------------------------------------------------
        # nodal coordinates:
        ops.node(1,0,0)     #  node , X Y
        ops.node(2,0,Lcol)
        
        # Single point constraints -- Boundary Conditions
        ops.fix(1,1,1,1)     #  node DX DY RZ
        
        # nodal masses:
        ops.mass(2,5.18,0.,0.)     #  node , Mx My Mz, Mass=Weight/g.
        
        # Define ELEMENTS -------------------------------------------------------------
        # define geometric transformation: performs a linear geometric transformation of beam stiffness
        # and resisting force from the basic system to the global-coordinate system
        ops.geomTransf('Linear',1)     #  associate a tag to transformation
        
        # element elasticBeamColumn eleTag iNode jNode A E Iz transfTag
        ops.element('elasticBeamColumn',1,1,2,3600000000,4227,1080000,1)
        
        # Define RECORDERS -------------------------------------------------------------
        ops.recorder('Node','-file',f'{dataDir}/DFree_Lcol{Lcol}.out','-time','-node',2,'-dof',1,2,3,'disp')     #  displacements of free nodes
        ops.recorder('Node','-file',f'{dataDir}/DBase_Lcol{Lcol}.out','-time','-node',1,'-dof',1,2,3,'disp')     #  displacements of support nodes
        ops.recorder('Node','-file',f'{dataDir}/RBase_Lcol{Lcol}.out','-time','-node',1,'-dof',1,2,3,'reaction')     #  support reaction
        ops.recorder('Element','-file',f'{dataDir}/FCol_Lcol{Lcol}.out','-time','-ele',1,'globalForce')     #  element forces -- column
        ops.recorder('Element','-file',f'{dataDir}/DCol_Lcol{Lcol}.out','-time','-ele',1,'deformation')     #  element deformations -- column
        
        # define GRAVITY -------------------------------------------------------------
        ops.timeSeries('Linear',1)     # timeSeries Linear 1;
        ops.pattern('Plain',1,1) # 
        ops.load(2,0.,-2000.,0.)     #  node , FX FY MZ -- superstructure-weight
        ops.wipeAnalysis()     # adding this to clear Analysis module 
        ops.constraints('Plain')     #  how it handles boundary conditions
        ops.numberer('Plain')     #  renumber dofs to minimize band-width (optimization), if you want to
        ops.system('BandGeneral')     #  how to store and solve the system of equations in the analysis
        ops.test('NormDispIncr',1.0e-8,6)     #  determine if convergence has been achieved at the end of an iteration step
        ops.algorithm('Newton')     #  use Newtons solution algorithm: updates tangent stiffness at every iteration
        ops.integrator('LoadControl',0.1)     #  determine the next time step for an analysis,   apply gravity in 10 steps
        ops.analysis('Static')     #  define type of analysis static or transient
        ops.analyze(10)     #  perform gravity analysis
        ops.loadConst('-time',0.0)     #  hold gravity constant and restart time
        
        # define LATERAL load -------------------------------------------------------------
        ops.timeSeries('Linear',2)     # timeSeries Linear 2;
        ops.pattern('Plain',2,2) # 
        ops.load(2,2000.,0.0,0.0)     #  node , FX FY MZ -- representative lateral load at top node
        
        # pushover: diplacement controlled static analysis
        ops.integrator('DisplacementControl',2,1,0.1)     #  switch to displacement control, for node 11, dof 1, 0.1 increment
        ops.analyze(1000)     #  apply 100 steps of pushover analysis to a displacement of 10
        
        print(f'pid {pid} of np={np} Analysis-{count} execution done')

    count +=1

print(f"pid {pid} of np={np} ALL DONE!!!")