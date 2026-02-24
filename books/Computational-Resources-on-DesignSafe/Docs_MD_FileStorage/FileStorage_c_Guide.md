# Storage Guide

## Quick Reference: Cheat Sheet

* **MyData** → Your personal notebook

  * Private, backed up, long-term
  * Best for personal files, scripts, tests

* **MyProjects** → Shared filing cabinet

  * Collaborative, long-term, curation-ready
  * Best for team data, archiving, publication

* **Work** → Scratchpad for active jobs

  * High-performance, temporary, not backed up
  * Best for staging inputs & writing job outputs

:::{admonition} **Rule of Thumb:**

* *If it’s important, back it up (MyData or MyProjects).*
* *If it’s temporary, run it in Work.*
:::

## Storage Decision Tree
**Which Storage Should I Use?**

* **Step 1: Are you running a compute job?**

  * **Yes** → Use **Work** for job inputs/outputs (fast I/O).
  * **No** → Continue ↓

* **Step 2: Do you need to share the data with a team?**

  * **Yes** → Use **MyProjects** (collaboration, publication).
  * **No** → Continue ↓

* **Step 3: Do you just need a private workspace?**

  * **Yes** → Use **MyData** (personal, backed up).
  * **No** → Continue ↓

* **Step 4: Is this public reference data you need to *read*?**

  * **Yes** → Access from **CommunityData** or **Published** (read-only).
  * **No** → Re-check your workflow; you may be mixing storage types.

**In short:**

* **Work** = jobs (fast, temporary).
* **MyProjects** = team (shared, curation-ready).
* **MyData** = personal (private, backed up).
* **Community/Published** = reference only.


## Common Mistakes to Avoid

:::{dropdown} Don’t leave important results in Work — it’s not backed up
   * Work is **not backed up** and may be purged without warning.
   * Always copy valuable results to MyProjects or MyData.
:::
:::{dropdown} Don’t use MyData for team projects — use MyProjects instead
   * Files in MyData are private unless explicitly shared.
   * Use MyProjects for collaboration.
:::
:::{dropdown} Don’t try to save to Community/Published — they’re read-only
   * These directories are **read-only**.
   * They are for reference only.
:::
:::{dropdown} Don’t run jobs directly from Corral — stage to Work first
   * Corral is network-mounted and slower for I/O-intensive workloads.
   * Always stage input/output to Work for active jobs.
:::


:::{dropdown} Don’t Use Work for long-term project storage
   * Work is high-performance but temporary.
   * Use MyProjects for durable project data.
:::

**Remember:** 
* Corral = archive
* Work = scratch
* Node-local = temporary runtime.

