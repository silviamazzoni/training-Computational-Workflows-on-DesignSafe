# Tapis on DesignSafe
by **Silvia Mazzoni**<br>
Applications Specialist @ DesignSafe<br>
January 2026

Tapis is a **network-based API** built on **REST architecture**, enabling users to manage computational jobs, data, and workflows across high-performance computing (HPC) and cloud systems — all through a consistent and secure interface.

* **API** = Application Programming Interface — a programming layer that allows different software tools to talk to each other.
* **Networked API** = APIs that communicate over a network (like the internet).
* **REST Architecture** = "REpresentational State Transfer" — a common architectural style for web services that uses standard HTTP methods (GET, POST, PUT, DELETE).

**Tapis Jobs** let you submit and run computational tasks on remote systems (HPC clusters, cloud VMs, containers) through a consistent API (Web Portal, Tapipy/Python, CLI, or direct HTTP). 

A job is a single execution of a registered Tapis App with your inputs, parameters, and resource requests. **Submitting a job** tells Tapis: “Run this app with these settings on that system.”

Tapis Jobs can be submitted to TACC via one of the following:
* **Web Portal** (forms)
* **Python (Tapipy)** (scripts/notebooks)
* **Tapis CLI** (command-language interface)
* **HTTP (cURL/JSON)**

Tapis handles: input staging, execution, status tracking, and result archiving.

You can also use Tapis to **query your jobs** during runtime (to check the status) or once they are completed (to check execution metadata and output data).



The following diagram shows the role of Tapis in your workflow: it connects your interface to the execution system.

<img src="../../../../shared/images/ComputeWorkflow.jpg" alt="Compute Environment" width="75%" />