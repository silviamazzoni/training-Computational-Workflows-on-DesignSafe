# Interfacing with Tapis
***Communicating with Tapis: API vs SDK***

Tapis is a powerful platform designed to support **remote job execution**, **data transfer**, and **workflow automation** across heterogeneous systems like supercomputers, cloud nodes, and containers.

At its core, the **Tapis Jobs API** allows users to:

* Submit computational jobs based on registered applications
* Monitor job status through a consistent lifecycle
* Retrieve outputs and logs after completion
* Automate workflows with job metadata, permissions, and archiving

Tapis Jobs are tightly integrated with **Tapis Systems** (where the job runs) and **Tapis Apps** (which define how it runs).




There are two main ways to interact with Tapis:
::::{dropdown} **1. Tapis SDK (*Tapipy*)**
*The **Tapis REST API** is the raw interface (HTTP-based)*

**Tapipy** is a Python SDK generated directly from the Tapis OpenAPI specification. It provides:

* Full coverage of the Tapis API
* Complete access to all Tapis endpoints and resources
* Methods that closely mirror the REST API structure
* Fine-grained control for advanced workflows

With Tapipy, you don’t need to manually construct HTTP requests, handle tokens, or parse raw JSON responses — the SDK manages these details for you.


An **SDK** (Software Development Kit) is a **collection of tools, libraries, documentation, and code examples** that help developers build software applications that interact with a specific platform, service, or system.

In simple terms:
*An SDK is a **developer toolbox** that makes it easier to program against an API or platform.*

* Wraps the full REST API into Python methods.
* Allows you to focus on your workflow logic, not protocol details.
* Tapipy is the Official Python SDK for Tapis v3.
    * Auto-generated from the Tapis OpenAPI spec (always current).
* Handles:

  * Authentication
  * Tokens
  * Headers
  * HTTP requests
  * Response parsing into Python objects


:::{dropdown} Example (using **Tapipy** SDK):

```python
    from tapipy.tapis import Tapis

    client = Tapis(base_url="https://tacc.tapis.io",
                   username="your-username",
                   password="your-password",
                   account_type="tacc")

    client.get_tokens()

    # Submit a job
    job_request = {
        "name": "example-job",
        "appId": "hello-world-1.0",
        "archive": True,
        "archiveSystemId": "tacc-archive",
        "archivePath": "your-username/job-output"
    }

    job = client.jobs.submitJob(body=job_request)
    print("Job ID:", job['id'])

    jobs = client.jobs.listJobs()
```

:::


::::

::::{dropdown} **2. Tapis API (REST API)**
*The **Python SDK** (**tapipy**) wraps that API into easy-to-use Python functions*

* The raw interface that powers everything behind the scenes.
* Uses standard web protocols (HTTP, HTTPS, GET, POST, PUT, etc.).
* You send requests directly to Tapis endpoints.
* Can be accessed using any language (Python, Java, curl, etc.)
* Requires you to:

  * Build request URLs
  * Add authentication headers
  * Manage tokens
  * Format request bodies (payloads) as JSON
  * Parse JSON responses
  * Handle HTTP errors and headers manually

:::{dropdown} Example (using **curl**):

```bash
    curl -X GET https://tacc.tapis.io/v3/jobs \
      -H "Authorization: Bearer <token>"
```
:::

::::


| Approach                 | Description                                                                                  | Who uses it?                                           |
| ------------------------ | -------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| **Tapis API (REST API)** | The raw interface exposed by Tapis via HTTP requests (URLs, headers, tokens, JSON payloads). | Advanced users, system integrators, non-Python clients |
| **Tapis SDK (Tapipy)**   | A Python library that wraps the API into easy-to-use Python functions.                       | Most application developers, researchers, students     |


## Why We **Recommend Tapipy**
*“The SDK uses the API under the hood — you don’t lose power, you just lose the pain.”*


| Feature          | Tapipy                              |
| ---------------- | ----------------------------------- |
| API coverage     | 100% (full Tapis API)             |
| Auto-generated   | Always current                    |
| Authentication   | Simplified                        |
| Request building | Pass Python dicts                 |
| Error handling   | Python exceptions                 |
| Suitable for     | Researchers, students, developers |

##  Summary

* SDK a toolkit that **simplifies programming** against a complex system like Tapis
* **Tapis API** = Low-level interface (web-based, language-agnostic)
* **Tapis SDK** = Python wrapper for the Tapis API (easier for developers)
* SDKs use the API under the hood but **hide the complexity** --  wrap APIs with user-friendly methods in a specific programming language

|                          | Tapis API  | Tapis SDK (Tapipy) |
| ------------------------ | ---------- | ------------------ |
| Language                 | Any        | Python             |
| Manual token handling    | Yes        | No                 |
| Raw HTTP requests        | Yes        | No                 |
| Recommended for training | ⚠ Advanced | ✅ Yes              |

