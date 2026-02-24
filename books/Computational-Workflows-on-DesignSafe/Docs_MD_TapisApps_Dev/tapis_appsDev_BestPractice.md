# Best Practices
***Best Practices for Tapis v3 App Deployment***

:::{dropdown} 1) Directory & Versioning Strategy

**Goal:** keep jobs reproducible while giving humans a simple place to grab “whatever is current.”

**One app, many versions (immutable)**

* Layout on your deployment system:

  ```
  apps/<app_id>/<version>/
  ```

  e.g., *apps/opensees-mp/1.0.0/*
* Treat each *<version>* directory as **immutable after registration**.
  If you need a change, **cut a new version** (e.g., *1.0.1*) and re-register.

**Use semantic versions (don’t register “latest”)**

* Prefer **SemVer**: *MAJOR.MINOR.PATCH* → *1.0.0*, *1.0.1*, *1.1.0*.
* **Do not** register an app version literally named *latest*. If *latest* moves, your old notebooks would silently run different code on re-submit.

**The “latest” convenience folder (what it is & how to use it)**

* Keep a **lightweight alias folder** for humans:

  ```
  apps/<app_id>/latest/
  ```

  This is **just a copy** of the newest version’s files—handy for browsing, reading wrappers, or quick manual tests.
* **Important:** you still register and submit jobs with a **pinned** semantic version (e.g., *appVersion: "1.2.3"*). The *latest/* folder is **not** an app version; it’s a browsable mirror.
* **Promotion workflow:**

  1. Upload & register *apps/<app_id>/<new_version>/…*
  2. Validate it (smoke tests)
  3. **Refresh** *apps/<app_id>/latest/* to **match** *<new_version>* (copy the files)
* Why copy (not symlink)? It avoids symlink support/permission quirks and keeps *latest/* portable.

**Mini-recipe → “promote to latest”**

* Create/update the folder, then upload the three core files again (from your working copy):

  ```bash
  tapis files mkdir designsafe.storage.default apps/<app_id>/latest
  tapis files upload app.json        designsafe.storage.default:apps/<app_id>/latest/app.json
  tapis files upload profile.json    designsafe.storage.default:apps/<app_id>/latest/profile.json
  tapis files upload tapisjob_app.sh designsafe.storage.default:apps/<app_id>/latest/tapisjob_app.sh
  ```

  *(If you keep examples/ or docs with the version, mirror those too.)*

:::

:::{dropdown} 2) Environments: dev → test → prod

**Two clean patterns—pick one and stick to it:**

* **Separate IDs per stage (most isolated)**

  ```
  opensees-mp-dev   / 0.9.x     # fast iteration, “okay to change”
  opensees-mp-test  / 1.0.0-rc1 # release candidate
  opensees-mp       / 1.0.0     # production
  ```

  Pros: zero confusion about what is prod. Cons: multiple appIds to manage.

* **Single ID, staged versions**

  ```
  opensees-mp / 1.0.0-rc1  # test
  opensees-mp / 1.0.0      # prod
  ```

  Pros: one appId. Cons: stricter process to prevent users from picking RCs.

**Across stages, only change what must differ:**

* *executionSystem*, SLURM queue, default node/core limits
* Container image tag or module set in *profile.json*

**Keep the input/parameter schema stable** from test → prod to avoid breaking users mid-upgrade.

:::


:::{dropdown} 3) Files to include per version

* *app.json* — App metadata + input schema + execution/deployment systems.
* *profile.json* — Environment prep on the execution system (modules, PATH, MPI launcher).
* *tapisjob_app.sh* — Runtime wrapper (load modules/container, *cd*, run, write exit code).
* **Optional but recommended**

  * *README.md* — What changed, usage notes, known issues.
  * *CHANGELOG.md* — Human-readable diff from the prior version.
  * *examples/* — Tiny, fast inputs for smoke tests.

**Tip:** keep container/module versions **pinned per app version** and echoed at runtime.
:::

:::{dropdown} 4) Permissions & Ownership

* Make the **versioned directories effectively read-only** after registration.
* Ensure the **app owner/team** retains write access to *apps/<app_id>/*.
* Prefer a **team/service account** as *owner* in *app.json* for continuity (people change; teams persist).
* If the app is shared broadly, store it on a **project or shared system** where the team has write access; point *deploymentSystem* there.

:::

:::{dropdown} 5) Registration & Immutability

* **Upload → register → freeze.**
  Don’t edit in place post-registration.
* Need a fix? **Bump version** (*1.0.1*) and re-register.
* Record the **registered app UUID** and (if applicable) the **git commit/tag** that produced the artifacts.

:::

:::{dropdown} 6) Validation Checklist (quick)

* *app.json* parses & includes: *id*, *version*, *executionSystem*, *deploymentSystem*, *runtime*, inputs/params.
* *profile.json* matches the **execution system**:

  * Modules exist; *OpenSees** or *python* path resolves.
  * MPI launcher (*ibrun*, *mpirun*, *srun*) is correct for that cluster.
* *tapisjob_app.sh*:

  * *set -e* (or explicit exit checks) and **always** write *${_tapisExecSystemOutputDir}/tapisjob.exitcode*.
  * Print environment and versions for provenance.
  * Use correct working dir & mounts (container binds or module context).
* **Smoke test** (tiny example):

  * Submits successfully, stages inputs, runs, captures output, archives, and surfaces **non-zero exits** clearly.

:::

:::{dropdown} 7) Consistent Inputs & Defaults

* Keep the schema **minimal and clear** (required vs optional).
* Provide safe **defaults** (queue, walltime, nodes/cores) so a novice can click “Run.”
* Document Tcl vs OpenSeesPy expectations (e.g., *mainProgram*, *tclScript*, *pyScript*) and how they map into your wrapper.

:::

:::{dropdown} 8) Separation of Concerns (why split files)

* *app.json* → **What** (contract): app identity, schema, systems, resources.
* *profile.json* → **Prepare**: modules/env for the execution system.
* *tapisjob_app.sh* → **Run**: container/module launch, scheduler integration, error plumbing.

This separation lets you tweak **runtime environment** without rewriting the app contract.

:::

:::{dropdown} 9) Container & Modules

* Prefer **versioned container tags**: *taccaci/opensees:2025.06* (not *:latest*).
* If using **modules**, pin exact versions in *profile.json* and **echo them** at job start.
* If you swap a container/module version, **cut a new app version** so jobs remain reproducible.

:::

:::{dropdown} 10) Provenance & Logging

* At job start, print:

  * app id & version
  * container image & tag (or module list with versions)
  * SLURM env (job id, node list), hostname
  * date/time, working directory
* On exit, always:

  * write an explicit **exit code**
  * summarize key outputs (or where they were archived)
* These make triage and user support much faster.

:::

### FAQ on *latest* vs versions (quick recap)

* **Q:** Can we register *appVersion: "latest"*?
  **A:** Avoid it—repro breaks when *latest* changes.
* **Q:** What’s the point of *apps/<app_id>/latest/* then?
  **A:** Human-friendly browsing and ad-hoc tests. Jobs still use pinned versions.
* **Q:** How do we keep *latest/* fresh?
  **A:** After promoting a new version, copy its files into *latest/* (don’t forget README/CHANGELOG/examples if you rely on them).

If you want, I can add a tiny Tapipy cell that **mirrors** *apps/<app_id>/<ver>/* → *apps/<app_id>/latest/* from your *local* working tree (simple and safe), or sketch a server-side copy loop if you prefer keeping it entirely on the storage system.
