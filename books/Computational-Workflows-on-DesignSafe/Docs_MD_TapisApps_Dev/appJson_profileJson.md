# app.json vs profile.json
***App Definition vs. Execution Profile (Tapis v3)***


Tapis v3 separates **what your app is** from **how its environment is prepared**:

* **app.json** — the *app definition*: ID, version, execution system, runtime, job type/parallelism, defaults, inputs/parameters.
* **profile.json** — the *execution environment profile*: modules to load, environment variables, pre/post shell snippets (if supported by your profile schema).

When you register an app, Tapis stores these as one app object. If you **do not** provide a *profile.json*, Tapis simply uses the *app.json* data as-is. You should **not** add "*modules*" or other profile-only fields to *app.json*.

> **Rule of thumb**
>
> * If you need *module load ...* or special environment variables → include a *profile.json*.
> * If your executable is already on *$PATH* (e.g., via a system module automatically loaded by your batch wrapper) or you run inside a container that encapsulates the environment → you can omit *profile.json*.

---

## Minimal, Valid Templates

### A. With *profile.json* (modules + env vars)

**app.json**

```json
{
  "id": "opensees-mp-s3-latest",
  "name": "OpenSeesMP",
  "version": "latest",
  "description": "Run OpenSeesMP on Stampede3",
  "owner": "your-username",
  "executionSystem": "designsafe.community.stampede3",
  "executionType": "HPC",
  "runtime": "LINUX",
  "jobType": "MPI",
  "parallelism": "PARALLEL",
  "defaultNodes": 1,
  "defaultProcessorsPerNode": 48,
  "defaultMaxRunTime": "01:00:00",
  "inputs": [
    {
      "id": "inputFile",
      "description": "Main OpenSees input script",
      "details": { "label": "Model File" },
      "required": true
    }
  ]
}
```

**profile.json**

```json
{
  "modules": ["hdf5", "opensees"],
  "envVariables": {
    "OMP_NUM_THREADS": "1"
  }
}
```

### B. Without *profile.json* (no modules needed)

**app.json**

```json
{
  "id": "opensees-mp-s3-latest",
  "name": "OpenSeesMP",
  "version": "latest",
  "description": "Run OpenSeesMP on Stampede3 (no modules needed)",
  "owner": "your-username",
  "executionSystem": "designsafe.community.stampede3",
  "executionType": "HPC",
  "runtime": "LINUX",
  "jobType": "MPI",
  "parallelism": "PARALLEL",
  "defaultNodes": 1,
  "defaultProcessorsPerNode": 48,
  "defaultMaxRunTime": "01:00:00",
  "inputs": [
    {
      "id": "inputFile",
      "description": "Main OpenSees input script",
      "details": { "label": "Model File" },
      "required": true
    }
  ]
}
```

*(No `profile.json` at all. Do **not** add `"modules": []` to `app.json` — that’s a profile field.)*

---

## How Tapis “Combines” Them Internally

After app registration, Tapis exposes a **single app record** that merges the definition and the environment profile. Conceptually, you’ll see fields from both. For illustration:

```json
{
  "id": "opensees-mp-s3-latest",
  "name": "OpenSeesMP",
  "version": "latest",
  "executionSystem": "designsafe.community.stampede3",
  "executionType": "HPC",
  "runtime": "LINUX",
  "jobType": "MPI",
  "parallelism": "PARALLEL",
  "defaultNodes": 1,
  "defaultProcessorsPerNode": 48,
  "defaultMaxRunTime": "01:00:00",
  "inputs": [
    { "id": "inputFile", "required": true, "details": { "label": "Model File" } }
  ],

  "profile": {
    "modules": ["hdf5", "opensees"],
    "envVariables": { "OMP_NUM_THREADS": "1" }
  }
}
```

If you omit `profile.json`, the `profile` portion is simply absent (or empty) in the combined record.

---

## Choosing: Include a Profile or Not?

| Scenario                                                                                                                            | Recommendation                                                                                  |
| ----------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| You must *module load opensees* or set *export VAR=...*                                                                             | Provide a *profile.json* with "*modules*" and "*envVariables*".                                 |
| Executable is already on *$PATH* (system module preloaded elsewhere), or you rely on a container image that has everything baked in | Omit *profile.json*. Simpler and less brittle.                                                  |
| You’re migrating from a containerized app to a system-module app (or vice versa)                                                    | Keep *app.json* stable; adjust *profile.json* to match the environment strategy.                |
| You want a “no-op” profile                                                                                                          | Either omit *profile.json*, or include an empty one like *{"modules": [], "envVariables": {}}*. |

---

## Common Pitfalls (and How to Avoid Them)

* **Putting profile fields into *app.json***
  Don’t add *"modules"* or *"envVariables"* to *app.json*. They belong in *profile.json*.
* **Forgetting modules on HPC**
  If the runtime wrapper (*tapisjob_app.sh*) expects *OpenSeesMP*` to exist but it’s not on *$PATH*, you’ll see “command not found.” Add the module in *profile.json* **or** switch to a container that includes it.
* **Omitting *defaultProcessorsPerNode* on MPI apps**
  For parallel apps, set realistic defaults (`48` for Stampede3 is a good starting point) and adjust at submit time as needed.

---

## Quick Reference: When to Use Each File

* ***app.json*** — Always required. Describes the app interface and execution basics.
* ***profile.json*** — Optional. Use only when you must tune the execution environment (modules, env vars).

---

## FAQ

**Q: Does Tapis “merge” *app.json* and *profile.json* automatically?**
**A:** Yes. On registration, Tapis stores both and presents a unified app record.

**Q: Can I just leave out *profile.json*?**
**A:** Yes—if you don’t need environment modules or env vars.

**Q: If I omit *profile.json*, should I add *"modules": []* to *app.json*?**
**A:** No. That field is not part of the *app.json* schema.

---

## Copy‑Paste Checklist

* [ ] Create *app.json* with ID, version, system, runtime, job type, defaults, inputs/params.
* [ ] Decide whether you need to *module load* or set env vars.

  * If **yes** → add a *profile.json* with *"modules"* / *"envVariables"*.
  * If **no** → omit *profile.json*.
* [ ] Register the app.
* [ ] Verify the combined record shows what you expect (inputs, defaults, and profile when present).
* [ ] Submit a small test job; check *.out/.err* logs to validate the environment is correct.

---

If you want, I can tailor the templates above to your ***opensees-mp-s3*** app conventions (IDs, owner, defaults) and your ***tapisjob_app.sh*** wrapper assumptions.
