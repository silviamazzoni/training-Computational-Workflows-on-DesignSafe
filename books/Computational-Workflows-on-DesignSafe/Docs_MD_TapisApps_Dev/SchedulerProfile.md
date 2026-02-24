# Scheduler Profile
**Execution Environment Setup *(optional but strongly recommended)***

A **scheduler profile** defines the *baseline execution environment* that TACC provides to your job **before** your wrapper script runs.
It is not part of your application code, but rather a system-level configuration that controls:

* How the job is launched on the HPC system
* What shell initialization is performed
* Whether the *module* command is available
* Which default modules—if any—are pre-loaded
* Whether TACC automatically loads compiler, Python, or MPI stacks

Most TACC apps use one of the built-in profiles, such as:

* ***tacc-no-modules***

  > Loads *no* modules automatically.
  > This is ideal for custom apps because your wrapper script decides exactly which modules to load (Python, OpenSees, HDF5, etc.).

* ***tacc-apptainer***, ***tacc-singularity***, etc.

  > Used for containerized workflows.

For our OpenSees/OpenSeesPy apps, we intentionally select:

```bash
--tapis-profile tacc-no-modules
```

This ensures:

1. We start with a **clean environment**
   (Avoids conflicts between system-loaded modules and user-requested modules.)

2. The wrapper script has **full control** over which modules are loaded.
   For example: *python/3.12.11*, *opensees*, *hdf5/1.14.4*, etc.

3. The app behaves **predictably and reproducibly**, regardless of user account or portal defaults.

If desired, users or developers may define a **custom scheduler profile** to preload certain modules or define custom environment variables, but for most HPC science workflows, *tacc-no-modules* is the cleanest and safest choice.


