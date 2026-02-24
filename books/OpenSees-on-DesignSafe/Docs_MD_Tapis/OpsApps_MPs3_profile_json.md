# profile.json
    
This file ensures the Stampede3 environment is correctly set up for OpenSeesMP.

## App-Definition File
:::{dropdown} **profile.json**
```
{
    "name": "OpenSees_default",
    "description": "Modules to load for the default version of OpenSees",
    "moduleLoads": [
        {
            "modulesToLoad": [
                "hdf5/1.14.4",
                "opensees"
            ],
            "moduleLoadCommand": "module load"
        }
    ],
    "hiddenOptions": [
        "MEM"
    ]
}
```
:::

## What It Does

| Field           | Meaning                                                  |
| --------------- | -------------------------------------------------------- |
| *moduleLoads*   | Loads necessary Stampede3 modules                        |
| *hiddenOptions* | Prevents Tapis GUI from showing certain runtime controls |

```json
{
  "name": "OpenSees_default",
  "description": "Modules to load for the default version of OpenSees",
  "moduleLoads": [
    {
      "modulesToLoad": [
        "hdf5/1.14.4",
        "opensees"
      ],
      "moduleLoadCommand": "module load"
    }
  ],
  "hiddenOptions": ["MEM"]
}
```

## Explanation

* *hdf5/1.14.4* — Ensures compatibility if your *.tcl* script uses HDF5 input/output
* *opensees* — Loads OpenSees and OpenSeesMP
* *MEM* hidden — hides editable memory setting in the portal UI (uses system default)


## Combined Summary

| File              | Purpose                                                          |
| ----------------- | ---------------------------------------------------------------- |
| *tapisjob_app.sh* | Runs OpenSeesMP with *ibrun*, handles job errors cleanly         |
| *app.json*        | Declares input/output structure, scheduler config, and job setup |
| *profile.json*    | Loads Stampede3 environment modules (*opensees*, *hdf5*)         |

Together, these enable a user to submit a **fully parallelized OpenSees simulation** using Tapis, either via the portal or from code.
