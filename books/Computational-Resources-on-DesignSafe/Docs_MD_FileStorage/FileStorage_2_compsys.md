# On Compute System
***Storage on Compute Systems (e.g., Stampede3)***

When running simulations or compute-intensive jobs, storing data directly on the compute system (Stampede3) offers **high-performance I/O** and fast access to data. 


* **Advantage**: Speed — ideal for active job execution and intermediate data.
* **Limitation**: System-bound — data is not universally accessible through DesignSafe's web portal or across platforms.

These storage options — **Home**, **Work**, and **Scratch** — are optimized for compute workflows, but are **tied to the specific system** and **not easily accessible from other environments**. 

## Stampede3 Storage: Home, Work, Scratch

Once your data is staged or results are ready to be processed, Stampede3 provides three directories optimized for specific compute-side tasks:

* ### **Home Directory (*$HOME*)**

  * Personal, backed-up storage for code, scripts, and setup files.
  * ⚠️ *Note: On Stampede3, the home directory is **not used heavily on DesignSafe** because it is tied to a specific compute system and not easily accessible from other environments.*
    
    :::{dropdown} Home Directory
    
    * **Path**: */home1/username*
    * **Usage**: Personal files, source code, small scripts, binaries, dotfiles, etc.
    * **Quota**: Limited (usually \~10–20 GB)
    * **Backups**: ✅ Yes, backed up regularly
    * **Performance**: Slower I/O (not meant for heavy data processing)
    
    *When to use it*:
    
    * Storing source code and configuration files
    * Software installation (user-level)
    * Submitting job scripts
    * Anything small and important you don’t want to lose
    
    :::

* ### **Work Directory (*$WORK* or *$WORK2*)**

  * Persistent, project-shared space; ideal for input/output files and datasets
  * ⚠️ *Note:You can access this directory from the Data Depot as well as from Jupyter Environements*
    
    :::{dropdown} Work Directory

    * **Path**: */work2/projects/{project_name}/username* or */work2/username*
    * **Usage**: Shared project files, medium-to-large datasets, intermediate job files
    * **Quota**: Project-based quota (often several TB)
    * **Backups**: ❌ Not backed up — **keep your own copies!**
    * **Performance**: Moderate — designed for collaborative use and longer-term storage than scratch
    
    *When to use it*:
    
    * Data shared among project members
    * Input/output files for simulations
    * Organizing project-specific directories
    * Anything too large for your home directory but not temporary
    
    :::

* ### **Scratch Directory (*$SCRATCH*)**

  * High-speed, temporary storage for job execution and intermediate data. Automatically purged after a period of inactivity.
  * **Tapis Jobs, such as the Web-Portal OpenSees Applications, are run here by default**
  * "The $SCRATCH file system, as its name indicates, is a temporary storage space. Files that have not been accessed* in ten days are subject to purge. Deliberately modifying file access time (using any method, tool, or program) for the purpose of circumventing purge policies is prohibited." [TACC Scratch Policy](https://docs.tacc.utexas.edu/hpc/stampede3/#scratchpolicy)
    
    :::{dropdown} Scratch Directory

    
    * **Path**: */scratch/username*
    * **Usage**: Temporary files for active jobs, large read/write operations
    * **Quota**: Large (often multiple TB) — but files are **purged automatically**
    * **Purge Policy**: Typically 10–30 days of inactivity
    * **Backups**: ❌ No backups
    * **Performance**: Fastest I/O
    
    *When to use it*:
    
    * Job scratch space (e.g., temp files during computation)
    * Short-term file staging
    * High-performance I/O operations
    * Large simulation output you don’t need long-term
    :::





## Summary Table

| Feature       | **Home**           | **Work**                             | **Scratch**           |
| ------------- | ------------------ | ------------------------------------ | --------------------- |
| Example Path          | */home1/username*  | */work2/projects/{project}/username* | */scratch/username*   |
| Size Limit    | Small (\~10–20 GB) | Large (per project)                  | Very large (multi-TB) |
| Backed up?    | ✅ Yes              | ❌ No                                 | ❌ No                  |
| Auto-deleted? | ❌ No               | ❌ No                                 | ✅ Yes (inactivity)    |
| Best for      | Code, config files | Input/output data, shared files      | Temp job files        |
| I/O Speed     | Slowest            | Moderate                             | Fastest               |

### Practical Example:

If you're running a simulation:

* Store your job script and code in **home**
* Stage your input files in **work**
* Run the job using **scratch** for temp outputs to maximize speed
* After the job finishes, move important results from **scratch** to **work**
* After that, you can decide where to move the data to a more permanent location on **corral**


### Navigating within Stampede3

If you have connected to the HPC directly via SSH, such as on Stampede3, you can use these quick navigation Shortcuts: *cdw*, *cdh*, *cds*

On **Stampede3**, TACC provides convenient **shell shortcuts** to quickly navigate between storage directories:

| Shortcut | Equivalent Command        | Description                        |
| -------- | ------------------------- | ---------------------------------- |
| **cdh**    | *cd $HOME*                | Goes to your **Home** directory    |
| **cdw**    | *cd $WORK* or *cd $WORK2* | Goes to your **Work** directory    |
| **cds**    | *cd $SCRATCH*             | Goes to your **Scratch** directory |

These are **shell functions** defined in your environment by default when you log in. You can use them from any location to quickly jump to your respective directories.

**Example**:

```
cdw     # Takes you to /work2/projects/myproject/username<br>
cdh     # Takes you to /home1/username<br>
cds     # Takes you to /scratch/username<br>
```

Use these commands often — they save time and reduce mistakes when working with multiple storage systems.


