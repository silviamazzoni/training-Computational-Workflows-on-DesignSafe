# Custom Tapis Apps
***Using Public Apps vs. Writing Your Own***

On DesignSafe, you have two productive ways to run work on HPC systems:

* **Use a public Tapis App** — pre-configured, maintained templates for common tools (e.g., OpenSees, OpenFOAM). Fastest path to results, minimal setup.
* **Author your own Tapis App** — a custom template you control (*wrapper* + *app.json* \[+ optional *profile.json*]) when you need different binaries, launch logic, inputs/parameters, or project-specific defaults.

**How to choose (at a glance):**
Start with a **public app** if your workflow fits its interface. Write a **custom app** when you need non-standard flags, containers/modules, pre/post steps, or a lab-specific interface you’ll reuse.

---

## A. Use an Existing (Public) App

Public apps on DesignSafe are vetted templates for common tools. They’re the fastest path to results.

**Where to find them**

* **Web Portal → Tools & Applications** to browse/search and read the app’s help page.
* In notebooks/CLI, grab the app’s ***appId*** (and optional version) from the portal and submit jobs programmatically.

**How to run effectively**

* Review the app’s **inputs** and **parameters** (from its schema).
* Start with a **small test case**; keep default resources, tune later.
* Prefer **stable/latest** versions shown in the catalog.
* Keep inputs on a Tapis-visible system (e.g., **MyData**, **Work**).

**When public apps are ideal**

* Your workflow matches the app interface.
* You want a **supported, reproducible** environment with minimal setup.
* You don’t need custom launch logic or unusual dependencies.

---
or
## B. Write Your Own App

Create a Tapis App when you need custom behavior, different software versions, or a specialized interface for your project.

**Building blocks**

1. **Wrapper** (e.g., *tapisjob_app.sh*): non-interactive, writes outputs to *$PWD*, handles launch (*ibrun*/*mpirun*/*srun*) and logging.
2. ***app.json* (required)**: app ID/version, execution system/type (HPC), job type (MPI/SERIAL), defaults (nodes/ppn/walltime), **inputs** & **parameters**.
3. ***profile.json* (optional)**: modules and env vars (or use containers).
4. **Tiny test dataset** for validation.

**Registration & sharing**

* Register via portal or API, then **share** with your project/team.
* For catalog visibility, follow DesignSafe’s review/publication process.

**Best practices**

* **Version** every change (e.g., *1.2.0*); keep a changelog; avoid breaking users.
* Use **Tapis URIs** and parameters—no hard-coded paths.
* Set **sensible defaults** (resources, inputs) and document them.
* Keep profiles minimal; prefer containers or a short *modules* list.
* Provide **clear labels/descriptions** so users don’t guess.

**When custom apps shine**

* New binaries/flags, custom pre/post steps, lab-specific UI.
* Automated **parameter sweeps**, ensembles, multi-stage workflows.
* A **reproducible** template your group can reuse.

---

## Quick Chooser

| Need                                    | Public app | Your app |
| --------------------------------------- | :--------: | :------: |
| Fast start with a standard tool         |      ✅     |          |
| Custom binaries, flags, or launch logic |            |     ✅    |
| Team-specific interface & defaults      |            |     ✅    |
| Minimal maintenance                     |      ✅     |          |
| Full control / special dependencies     |            |     ✅    |
