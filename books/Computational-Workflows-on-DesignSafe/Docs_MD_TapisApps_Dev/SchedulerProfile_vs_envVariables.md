#  Scheduler vs. envVariables
**Scheduler Profiles vs. envVariables**
    
Although both **Scheduler Profiles** and ***envVariables*** influence the job environment, they operate at *different stages* and serve *different purposes*.



## A. Scheduler Profiles (system-level initialization)

**Executed by TACC *before* your wrapper script runs.**

They control:

* How the compute node is initialized
* Whether the *module* command is available
* Whether *any* default modules (Python, MPI, compilers) are preloaded
* Job-launching behavior (*srun*, *ibrun*, environment hygiene, etc.)

A scheduler profile is **owned by the execution system**, not by your app.

**Example:**
*--tapis-profile tacc-no-modules*
→ Start with a *completely clean* environment, no modules preloaded.

**Key Concept:**

> Scheduler Profiles configure the *system* before your app starts executing.

---
## B. *envVariables* in *app.json* (app-level configuration

**Passed directly into your running job and visible within *tapisjob_app.sh*.**

They allow the app user (or the app developer) to express configuration options such as:

* Which modules to load (*MODULE_LOADS_LIST*)
* Which pip packages to install (*PIP_INSTALLS_LIST*)
* Whether to copy OpenSeesPy (*GET_TACC_OPENSEESPY*)
* MPI/serial toggle (*UseMPI*)
* Paths for input copying or output movement

These variables appear in your wrapper script like:

```bash
echo "MODULE_LOADS_LIST = ${MODULE_LOADS_LIST}"
```

and are fully controlled by the app developer or job submitter—not by TACC.

**Key Concept:**

> *envVariables* configure *your application’s behavior*, not the system.



## Summary

**Scheduler Profiles** initialize the compute node environment,
while ***envVariables*** configure how *your app* behaves within that environment.


