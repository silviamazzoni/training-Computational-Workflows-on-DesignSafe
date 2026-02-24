# establish_tms_credentials()
***establish_tms_credentials(tapis, system_id: str, username: str)***

**This function is run only the first time you connect to a specific system, such as Stampede3, on TACC.**

The functions *establish_tms_credentials* and *remove_tms_credentials* help **manage your Tapis system user credentials on a given system**, like *designsafe.storage.default* or a specific compute resource.

They’re essential when you need to run jobs, transfer files, or otherwise authenticate to systems registered in Tapis using **TMS\_KEYS authentication** (the typical model on DesignSafe).

---

This function ensures that the specified user (**username**) has valid system credentials set up on the specified **system_id**. It:

1. **Checks if credentials already exist**

   * Calls *tapis.systems.checkUserCredential*.
   * If they exist, prints a message and exits.

2. **If credentials are missing:**

   * It catches an *UnauthorizedError*.
   * Looks up the system definition using *getSystem*.
   * If the system uses *TMS_KEYS* as its default authentication, it calls *createUserCredential* to generate new TMS keys.

3. Prints confirmation that the credentials are established.

---

#### Typical usage scenario

* You must have credentials on a system (like SSH keys or TMS managed keys) to submit jobs or move files.
* This function **automates creating those credentials if they’re missing**, so your workflows don’t fail.


---

### Smart handling

* Only creates new credentials if they don’t already exist.
* Catches **UnauthorizedError** specifically, which is what Tapis raises when the user has no credentials on the system.

---


###  Managing Tapis system user credentials

These two helper functions let you easily manage your credentials on a Tapis-registered system (like a storage system or compute resource).

| Function                     | What it does |
|-------------------------------|--------------|
| **establish_tms_credentials** | Ensures user credentials exist on a Tapis system (creates them if missing). Checks if the user already has credentials on the given system. <br> If missing, automatically creates new TMS keys (for systems using *TMS_KEYS*). |
| **remove_tms_credentials**    | Removes user credentials from a Tapis system. Deletes the user’s credentials from the specified system. Useful for cleanup or resetting keys. |

---

####  Typical workflow

```python
# Ensure credentials are set up before running jobs or moving files
establish_tms_credentials(tapis, system_id="designsafe.storage.default", username="jdoe")

# Later, if needed, clean up
remove_tms_credentials(tapis, system_id="designsafe.storage.default", username="jdoe")
````

---

This makes it easy to prepare (or reset) your access to Tapis systems from your scripts or notebooks, without having to manually generate or manage SSH/TMS keys.


#### Files
You can find these files in Community Data.

```{dropdown} establish_tms_credentials.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Tapis/establish_tms_credentials.py
:language: none
```
