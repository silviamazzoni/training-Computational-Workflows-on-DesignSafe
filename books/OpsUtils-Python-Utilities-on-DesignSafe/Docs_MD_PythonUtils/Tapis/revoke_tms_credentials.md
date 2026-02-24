# revoke_tms_credentials()
***revoke_tms_credentials(tapis, system_id: str, username: str)***

**You will, likely, never need to use this function!!**

The functions *establish_tms_credentials* and *revoke_tms_credentials* help **manage your Tapis system user credentials on a given system**, like *designsafe.storage.default* or a specific compute resource.

They’re essential when you need to run jobs, transfer files, or otherwise authenticate to systems registered in Tapis using **TMS\_KEYS authentication** (the typical model on DesignSafe).


---

## Typical usage scenario

* You must have credentials on a system (like SSH keys or TMS managed keys) to submit jobs or move files.
* This function **automates creating those credentials if they’re missing**, so your workflows don’t fail.



This function does the reverse: it **deletes the user’s credentials on that system** by calling:

```python
tapis.systems.revoke_tms_credentials(systemId=system_id, userName=username)
```

This is useful for cleaning up credentials (for security or to reset them).

---

## Example usage

```python
establish_tms_credentials(tapis, system_id="designsafe.storage.default", username="jdoe")
# Will print status, and create TMS credentials if needed.

revoke_tms_credentials(tapis, system_id="designsafe.storage.default", username="jdoe")
# Cleans them up.
```

---

## Smart handling

* Only creates new credentials if they don’t already exist.
* Catches `UnauthorizedError` specifically, which is what Tapis raises when the user has no credentials on the system.

---


##  Managing Tapis system user credentials

These two helper functions let you easily manage your credentials on a Tapis-registered system (like a storage system or compute resource).

| Function                     | What it does |
|-------------------------------|--------------|
| **establish_tms_credentials** | Ensures user credentials exist on a Tapis system (creates them if missing).. Checks if the user already has credentials on the given system. <br> If missing, automatically creates new TMS keys (for systems using `TMS_KEYS`). |
| **revoke_tms_credentials**    | Revokes user credentials from a Tapis system. Deletes the user’s credentials from the specified system. Useful for cleanup or resetting keys. |

---

##  Typical workflow

```python
# Ensure credentials are set up before running jobs or moving files
establish_tms_credentials(tapis, system_id="designsafe.storage.default", username="jdoe")

# Later, if needed, clean up
revoke_tms_credentials(tapis, system_id="designsafe.storage.default", username="jdoe")
````

---

This makes it easy to prepare (or reset) your access to Tapis systems from your scripts or notebooks, without having to manually generate or manage SSH/TMS keys.

## Files
You can find these files in Community Data.
~/CommunityData/OpenSees/TrainingMaterial/training-OpenSees-on-DesignSafe/OpsUtils

```{dropdown} revoke_tms_credentials.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Tapis/revoke_tms_credentials.py
:language: none
```


