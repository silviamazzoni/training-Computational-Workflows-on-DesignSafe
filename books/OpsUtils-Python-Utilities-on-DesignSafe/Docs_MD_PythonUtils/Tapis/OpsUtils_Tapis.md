# Tapis OpsUtils

This module provides a suite of Python helper functions specifically designed to **simplify working with the Tapis platform**. These functions make it easier to connect, query, and manage jobs and data on DesignSafe or any Tapis-enabled system.

Each function in this collection includes:

- A clear explanation of **what the function does** and **why it’s valuable** for your workflows.
- A summary of **its inputs and outputs**, helping you quickly understand how to integrate it into your own scripts.
- The complete function code, ready to use, adapt, or extend.

All examples are embedded in **interactive Jupyter notebooks**, so you can experiment, adjust parameters, and see live results—making it easy to incorporate them into your projects.

You can find these utilities in:
~/CommunityData/OpenSees/TrainingMaterial/training-OpenSees-on-DesignSafe/OpsUtils

Add the following to your Jupyter Notebook or python script:

```
import sys,os
PathOpsUtils = os.path.expanduser('~/CommunityData/OpenSees/TrainingMaterial/training-OpenSees-on-DesignSafe/OpsUtils')
if not PathOpsUtils in sys.path: sys.path.append(PathOpsUtils)
from OpsUtils import OpsUtils
```
