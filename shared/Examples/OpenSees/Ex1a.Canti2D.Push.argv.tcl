# OpenSees Ex1a.Canti2D.Push.argv.tcl

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

set NodalMass 5.18
set dataDir DataTCL;                # set up name of data directory
set LcolList "100 120 200 240 300 360 400 480"

if {[llength $argv]>0} {
    puts "Command-Line Arguments (argv): $argv"
    # OpenSees Ex1a.Canti2D.Push.argv.tcl --NodalMass 5.18 --LcolList "100 120 200 240 300 360 400 480" --outDir outData33
    # OpenSees Ex1a.Canti2D.Push.argv.tcl --NodalMass 5.18 --LCol 100 --outDir outData133
    foreach {label value} $argv {
        if {$label == "--NodalMass"} {set NodalMass $value}
        if {$label == "--LCol"} {set LcolList "$value"}
        if {$label == "--LcolList"} {set LcolList $value}
        if {$label == "--outDir"} {set dataDir $value}
    }
}


puts "NodalMass $NodalMass"
puts "LcolList $LcolList"

puts "Saving results to: $dataDir"
file mkdir $dataDir



# ----------------------------------------------


set count 0;
foreach Lcol $LcolList {
    
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
    mass 2 $NodalMass 0. 0.;		# node#, Mx My Mz, Mass=Weight/g.
    
    # Define ELEMENTS -------------------------------------------------------------
    # define geometric transformation: performs a linear geometric transformation of beam stiffness 
    #	and resisting force from the basic system to the global-coordinate system
    geomTransf Linear 1;  		# associate a tag to transformation
    
    # connectivity: (make A very large, 10e6 times its actual value)
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
    
    puts "Analysis-${count} execution done"

    incr count 1;
}

puts "ALL DONE!!!"
