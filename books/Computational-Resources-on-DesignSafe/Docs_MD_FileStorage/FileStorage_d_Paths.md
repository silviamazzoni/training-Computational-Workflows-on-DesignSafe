# File Storage


## DesignSafe Storage Path Examples

* **JupyterHub**
    
    Mounted paths, accessible directly in the notebook file browser. In JupyterHub, **all storage** systems have the same base path, making it very practical.
    
    | Type            | Example Path                            |
    | --------------- | --------------------------------------- |
    | MyData          | */home/jupyter/MyData/*                 |
    | Work            | */home/jupyter/Work/stampede3/*         |
    | Community       | */home/jupyter/CommunityData/*          |
    | MyProjects      | */home/jupyter/MyProjects/PRJ-...*      |
    | NHERI Published | */home/jupyter/NHERI-Published/PRJ-...* |
    | NEES Published  | */home/jupyter/NEES/*                   |


  
* **Stampede3**
    
    Traditional HPC with **absolute UNIX paths**. These are the paths you’ll use when:
    
    * SSH’ing into Stampede3
    * Writing batch scripts or Tapis job submissions
    
    | Type    | Example Path                         |
    | ------- | ------------------------------------ |
    | Home    | */home1/yourgroupid/jdoe/*           |
    | Work    | */work2/yourgroupid/jdoe/stampede3/* |
    | Scratch | */scratch/yourgroupid/jdoe/*         |
    
    To confirm your actual paths on the system:
    
    ```bash
    cd $HOME && pwd       # → /home1/05072/silvia
    cd $WORK && pwd       # → /work2/05072/silvia/stampede3
    cd $SCRATCH && pwd    # → /scratch/05072/silvia
    ```