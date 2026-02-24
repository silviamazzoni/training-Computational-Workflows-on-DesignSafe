# Tapis App Templates

Every Tapis App that you run on DesignSafe—such as OpenSeesMP or OpenSeesSP—is based on an underlying **Tapis App template**. These templates define how an application is configured and executed within the Tapis ecosystem. They provide the foundational logic that allows scientific applications to be run in a consistent and portable way across different HPC systems.

Tapis App templates are structured collections of files that include everything needed to describe and launch a job: what executable to run, what inputs and parameters are required, and how to handle outputs. While users never need to see the templates directly, they are the reason apps can be reused across interfaces like the web portal, Jupyter notebooks, or programmatic workflows.

You can browse official and example templates—including those used for OpenSees—on GitHub at: [github.com/TACC/WMA-Tapis-Templates](https://github.com/TACC/WMA-Tapis-Templates)


## Purpose of App Templates

Tapis App templates serve as blueprints for building apps that can be registered with the Tapis system. They:

* Standardize how software is exposed and run on HPC resources
* Enable reproducibility and sharing of complex workflows
* Support automated job submission from web portals, APIs, and notebooks

A typical template includes:

* **JSON descriptor files** that define the app interface (inputs, parameters, outputs)
* **Shell scripts or wrapper scripts** that assemble and launch the computation
* **README or metadata files** to document how the app should be used

By using templates, institutions like TACC and DesignSafe maintain a robust, consistent catalog of scientific applications that users can access with minimal setup and no need for system-level knowledge.

## Extending Tapis: Create Your Own App Templates

In addition to using apps published by DesignSafe or TACC, advanced users can also **write their own Tapis app templates**. This means you can package your own scripts, analysis tools, or simulation codes—along with a custom wrapper and configuration—into a fully functional Tapis App.

Once you've created your app template, you can register it with Tapis and submit jobs just like with the built-in apps. This is especially useful for domain-specific workflows, teaching tools, or research pipelines that require precise control or repeatability.

If you want to get started, the [WMA-Tapis-Templates GitHub repository](https://github.com/TACC/WMA-Tapis-Templates) contains examples you can copy and adapt to your needs.



## Why This Matters for Scientific Workflows

The use of templates is a cornerstone of scalable and reproducible research computing. For users, this means:

* Fewer errors and misconfigurations thanks to automated input/output handling
* Seamless integration with interfaces like Jupyter, the DesignSafe web portal, or scripted APIs
* Clear separation between domain-specific logic (your science) and infrastructure-specific details (job scripts, scheduler flags, data staging)

Most importantly, Tapis App templates enable researchers to **focus on science**, not infrastructure—while ensuring jobs run reliably and reproducibly across systems.

But the value of templates extends beyond just using pre-built apps. If you're a researcher, educator, or tool developer, you can **create and register your own Tapis apps**. This allows you to:

* Package your custom scripts, binaries, or modeling pipelines for repeatable execution
* Automate complex workflows that would otherwise require manual coordination
* Share standardized tools across a lab, research collaboration, or student group
* Port your applications across different HPC systems without rewriting job logic

Writing your own app template gives you **full control over how your code is staged, executed, and monitored**—all while benefiting from the job handling, data movement, and user interface layers that Tapis provides.

In short, Tapis makes it easier not only to run existing scientific tools but also to **operationalize your own research methods** for high-throughput or collaborative computing.


