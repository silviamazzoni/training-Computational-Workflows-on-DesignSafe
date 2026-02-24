# OpenSees

**OpenSees** was conceptualized, designed, and developed with **parallel computing** as a core objective. Parallel computing means leveraging multiple processors to work simultaneously — not only on independent tasks but also on tightly coupled problems where processors exchange information during execution.

From these design principles grew **three major OpenSees applications (plus one Python interface)**, each optimized for different computational strategies and user needs:

1. **OpenSees (Sequential / Single-Core)**
2. **OpenSeesSP (Shared Memory Parallel)**
3. **OpenSeesMP (Distributed Memory Parallel)**
4. **OpenSeesPy (Python Interface)**

## Which OpenSees to run on DesignSafe?

There are a few main applications, each with its own use case.
* **Sequential Application:**
  1. **OpenSees** is the simplest application:
     - Regular OpenSees  
     - Single core and is easy to use.
     - Best for testing models, debugging, or smaller problems.
     - It's your starting place and can easily meet most project needs.

* **Parallel Applications:**
  1. **OpenSeesSP** is the *Single Parallel Interpreter* application:
     - Runs on a single node using multiple processors.
     - The single processor distributes a large model to the remaining processors for faster solution strategies. -- **Shared-Memory Parallel**
     - This application allows you to run very large models with ease because it automates the model decomposition with no need for input from the user.
     - Efficient for models that scale well with shared memory.
     - This application may not be available on OpenSeesPy

  2. **OpenSeesMP** is the *Multiple Parallel Interpreters* application:
     - It is the most versatile parallel application.
     - Runs across multiple nodes using MPI (message passing).
     - It runs all the processors in parallel, each executing the same script containing individual instructions for each processor.
     - This is the most powerful OpenSees application by giving the user full control of the job.
     - Two types of parallelization:
       1. Manual Model Decomposition (automated in OpenSeesSP) -- **Shared-Memory Parallel**
       2. Distributed parametric analyses. -- **Distributed-Memory Parallel**
     - Best for very large simulations that require distributed computing power.
     - Improve efficiency with Load Balancing (inter-processor communication)

* **kinda-Both**
  1. **OpenSeesPy (Python Interface)**
     - Provides a Pythonic interface to the OpenSees kernel.
     - Allows seamless integration with Python libraries (NumPy, SciPy, pandas, matplotlib, etc.), making it easier to script, postprocess, and automate workflows.
     - OpenSeesPy has been added to the DesignSafe Web Portal and Tapis Applications.
     - You can run OpenSeesPy in both Sequential or Parallel environment.
     - There are several ways to run OpenSeesPy in the parallel environment.
     - Running OpenSeesSP in OpenSeesPy requires some verification since it is environment-dependent. This is beyond the scope of this traning content.
     - Domain decomposition "should be possible" in OpenSeesPy.

## Quick-Decision Matrix for OpenSees Applications


| Model Size     | Analysis Parameters | Sequential OpenSees          | Shared-Memory Parallel     | Distributed-Memory Parallel            |
|----------------|---------------------|-------------------------------|------------------------------------------------|--------------------------------------------------|
| small–medium   | none–few            | ✅ Recommended                | 🚩 Element Robustness                      | ⏳ Extra time to set up the script             |
| small–medium   | many                | ⏳ Wait Time                   | 🚩 Element Robustness                      | ✅ Recommended                                    |
| medium–large   | none–few            | ⛔ Too Slow                   | ✅ Recommended                                  | ✅ Recommended + ⚠️ Manual Scripting              |
| medium–large   | many                | ⛔ Too Slow                   | 🚩 Element Robustness + ⛔ Too Slow             | ✅ Recommended + ⚠️ Manual Scripting              |
| very large     | none–few            | ⛔ Too Slow                   | ✅ Recommended                                  | ✅ Recommended + ⚠️ Manual Scripting              |
| very large     | many                | ⛔ Too Slow                   | ✅ Recommended 1 analysis/job                           | ✅ Recommended + ⚠️ Manual Scripting              |

Legend:
- ✅ Recommended solution  
- ⏳ Additional wait time due to HPC queue makes it a weak solution  
- 🚩 Requires ensuring element robustness in OpenSeesSP (weak solution)  
- ⚠️ Manual domain decomposition requires extra scripting effort  
- ⛔ Additional run time due to single-threaded execution makes it a bad solution  