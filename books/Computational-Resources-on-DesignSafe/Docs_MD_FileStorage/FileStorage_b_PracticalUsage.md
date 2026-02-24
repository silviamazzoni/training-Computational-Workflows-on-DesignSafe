# Practical Usage

## Using MyData, MyProjects, and Work

Each of the three main storage areas has a distinct role. Selecting the correct one ensures efficiency, collaboration, and data integrity.

### Overview Table

| Storage Area   | Purpose                                     | Access                                                    | Persistence                          | Performance |
| -------------- | ------------------------------------------- | --------------------------------------------------------- | ------------------------------------ | ----------- |
| **MyData**     | Personal storage                            | Private (owner only, unless shared)                       | Long-term, backed up                 | Standard    |
| **MyProjects** | Project-based collaborative storage         | Shared with project team                                  | Long-term, archival, and publication | Standard    |
| **Work**       | High-performance scratch space for HPC jobs | Accessible from compute nodes, Data Depot, and JupyterHub | Long-term, **not backed up**         | High        |

---

:::{dropdown} **MyData**
*Personal private storage space.*

* For input files, scripts, outputs, notes, small datasets.
* Only visible to you unless shared.
* Long-term persistence; backed up.
* Best for: early-stage work, drafts, personal scripts/tools, small tests.

***Use MyData when you’re working solo or building/testing something privately.***
:::

:::{dropdown} **MyProjects**
*Collaborative project-based storage.*

* Linked to a DesignSafe project ID.
* Accessible to all project members.
* Supports team data sharing, curation, and publication.
* Long-term, archival storage with DOI assignment for public release.
* Best for: collaborative results, large experiments, or data prepared for publication.

***Use MyProjects when collaborating, sharing, or curating data for publication.***
:::

:::{dropdown} **Work**
*Temporary high-performance scratch storage.*

* Optimized for active HPC jobs.
* Mounted directly to compute nodes for fast I/O.
* Not backed up — files may be lost if not copied out.
* Best for: staging large inputs, writing job outputs, temporary intermediates.

***Use Work for runtime I/O only. Always move important results to MyProjects or MyData after jobs complete.***
:::

---

## Typical Workflow Example

1. **Prepare input files and test scripts** → store in **MyData**
2. **Share input files with project team** → upload to **MyProjects**
3. **Transfer large datasets to Work** before running HPC jobs
4. **Run HPC jobs** → read/write to **Work**
5. **After jobs complete:**

   * Copy important files back to **MyProjects** (collaboration/curation).
   * Copy personal results back to **MyData**.
   * Let temporary files expire from **Work**.
