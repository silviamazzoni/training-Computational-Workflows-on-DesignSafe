# mpiexec -np 3 OpenSeesMP Ex1a_verymany.Canti2D.Push.mp.tcl

############################################################
#  EXAMPLE: 
#       Ex1a.Canti2D.Push.tcl
#          for OpenSees.exe (tcl)
#  --------------------------------------------------------#
#  by: Silvia Mazzoni, 2020
#       silviamazzoni@yahoo.com
############################################################
# This file was obtained by updating the Tcl script in the original examples manual
# You can find the original Examples:
# https://opensees.berkeley.edu/wiki/index.php/Examples_Manual
# Original Examples by By Silvia Mazzoni & Frank McKenna, 2006, in Tcl
############################################################
# --------------------------------------------------------------------------------------------------
# Example 1. cantilever 2D
# static pushover analysis with gravity.
# all units are in kip, inch, second
# elasticBeamColumn ELEMENT
#			Silvia Mazzoni & Frank McKenna, 2006
#
#    ^Y
#    |
#    2       __ 
#    |         | 
#    |         | 
#    |         | 
#  (1)      36'
#    |         | 
#    |         | 
#    |         | 
#  =1=    ----  -------->X
#
#

if {[llength $argv]>0} {
    puts "Command-Line Arguments (argv): $argv"
}

set pid [getPID]
set np [getNP]
if {$pid < 20} {
    puts "pid $pid of np=$np  started (showing only first 20)"
    if {[llength $argv]>0} {
        puts "pid $pid of np=$np  Command-Line Arguments (argv): $argv"
    }
}
        
# set LcolList "100 120 200 240 300 360 400 480"

set LcolList ""
# Define the range and number of elements
set start 10.0
set end 1000.0
set Npoints 1000

# puts "Npoints=$Npoints"

# Calculate the step size
set step [expr {($end - $start) / ($Npoints - 1)}]
set step [expr {int(int($step)+1)}]

# puts step_$step

# Generate the list
for {set i 0} {$i < $Npoints} {incr i} {
    set value [expr {$start + $i * $step}]
    lappend LcolList $value
}

if {$pid==0} {
    puts "pid $pid of np=$np  Npoints=$Npoints, step=$step"
    puts "pid $pid of np=$np  LcolList = $LcolList"
    set outfile1 [open "LcolList.out" w+]
    foreach Lcol $LcolList {
        puts $outfile1 $Lcol
    }
    close $outfile1
}

# ----------------------------------------------
set dataDir DataTCLmp;                # set up name of data directory
file mkdir $dataDir; # create data directory

set count 0;
foreach Lcol $LcolList {
    # check if count is a multiple of pid : "is it its turn?"
    if {[expr $count % $np] == $pid} {
        if {$pid < 20} {
           puts "pid=$pid Lcol=$Lcol count=$count"
        }
        # SET UP ----------------------------------------------------------------------------
        wipe;						# clear opensees model
        model basic -ndm 2 -ndf 3;	# 2 dimensions, 3 dof per node
        
        # define GEOMETRY -------------------------------------------------------------
        # nodal coordinates:
        node 1 0 0;				# node#, X Y
        node 2 0 $Lcol
        
        # Single point constraints -- Boundary Conditions
        fix 1 1 1 1; 			# node DX DY RZ
        
        # nodal masses:
        mass 2 5.18 0. 0.;		# node#, Mx My Mz, Mass=Weight/g.
        
        # Define ELEMENTS -------------------------------------------------------------
        # define geometric transformation: performs a linear geometric transformation of beam stiffness 
        #	and resisting force from the basic system to the global-coordinate system
        geomTransf Linear 1;  		# associate a tag to transformation
        
        # connectivity: (make A very large, 10e6 times its actual value)
        # element elasticBeamColumn $eleTag $iNode $jNode $A $E $Iz $transfTag
        element elasticBeamColumn 1 1 2 3600000000 4227 1080000 1;	
        
        # Define RECORDERS -------------------------------------------------------------
        recorder Node -file ${dataDir}/DFree_Lcol${Lcol}.out -time -node 2 -dof 1 2 3 disp;			# displacements of free nodes
        recorder Node -file ${dataDir}/DBase_Lcol${Lcol}.out -time -node 1 -dof 1 2 3 disp;			# displacements of support nodes
        recorder Node -file ${dataDir}/RBase_Lcol${Lcol}.out -time -node 1 -dof 1 2 3 reaction;		# support reaction
        recorder Element -file ${dataDir}/FCol_Lcol${Lcol}.out -time -ele 1 globalForce;			# element forces -- column
        recorder Element -file ${dataDir}/DCol_Lcol${Lcol}.out -time -ele 1 deformation;			# element deformations -- column
        
        
        # define GRAVITY -------------------------------------------------------------
        timeSeries Linear 1;
        pattern Plain 1 1 {
           load 2 0. -2000. 0.;			# node#, FX FY MZ --  superstructure-weight
        }
        constraints Plain;     			# how it handles boundary conditions
        numberer Plain;					# renumber dof's to minimize band-width (optimization), if you want to
        system BandGeneral;				# how to store and solve the system of equations in the analysis
        test NormDispIncr 1.0e-8 6 ; 	# determine if convergence has been achieved at the end of an iteration step
        algorithm Newton;				# use Newton's solution algorithm: updates tangent stiffness at every iteration
        integrator LoadControl 0.1;		# determine the next time step for an analysis, # apply gravity in 10 steps
        analysis Static					# define type of analysis static or transient
        analyze 10;						# perform gravity analysis
        loadConst -time 0.0;			# hold gravity constant and restart time
        
        # define LATERAL load -------------------------------------------------------------
        timeSeries Linear 2;
        pattern Plain 2 2 {
           load 2 2000. 0.0 0.0;		# node#, FX FY MZ -- representative lateral load at top node
        }
        
        # pushover: diplacement controlled static analysis
        integrator DisplacementControl 2 1 0.1;		# switch to displacement control, for node 11, dof 1, 0.1 increment
        analyze 1000;								# apply 100 steps of pushover analysis to a displacement of 10
        
        if {$pid < 20} {
            puts "pid $pid of $np Analysis-${count} execution done"
        }
        
        
    }
    incr count 1;
}

if {$pid < 20} {
    puts "pid $pid ALL DONE!!!"
}
