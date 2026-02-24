# Python Utilities on DesignSafe
***OpsUtils: Python Library on DesignSafe***

by **Silvia Mazzoni**<br>
January 2026


**OpsUtils()** is a module that brings together all the Python functions we’ve developed and integrated into these training modules.  
They are designed to make your work with DesignSafe, Tapis, OpenSees, and general Python workflows **simpler, faster, and more robust**.

All of these functions are stored under **CommunityData** and organized so that you can import them just like a regular Python module.  
The only difference is that you also specify the location where these functions live. Here’s how to import them:

**NOTE: Since we are continutally developing these utilities, they are not all documented or have updated documentation**


```python
# Local Utilities Library
import sys,os
PathOpsUtils = os.path.expanduser('~/CommunityData/OpenSees/TrainingMaterial/training-OpenSees-on-DesignSafe/OpsUtils')
if not PathOpsUtils in sys.path: sys.path.append(PathOpsUtils)
from OpsUtils import OpsUtils
````

Then simply call any function by prefixing with the package name:

```python
OpsUtils.functionName(input)
```


## 1. Miscellaneous Utilities

This collection of functions provides general-purpose helpers that you’ll find scattered throughout the training notebooks.
They handle a wide range of tasks, from flattening complex dictionaries to pretty-printing outputs in your Jupyter environment.

For each function, you’ll find:

* A clear description of what it does and why it’s useful.
* Its inputs and outputs explained in detail.
* The complete function code.
* All presented in **interactive notebooks**, ready for you to explore and adapt.


## 2. Tapis Utilities

These are specialized functions designed to make interacting with the **Tapis platform** straightforward and powerful.
They handle everything from authenticating and managing your tokens, to querying jobs and downloading outputs.

Just like the general utilities, each Tapis function is fully documented with:

* A summary of what it does and how it helps streamline your Tapis workflows.
* Details on inputs and outputs.
* The exact code you can drop into your own projects.




---
  
:::{include} TAILS.md
:::