# Computational Workflows on DesignSafe
***Understanding Interfaces, Middleware, and Execution Environments***

by **Silvia Mazzoni**<br>
January 2026

DesignSafe provides a comprehensive cyberinfrastructure for conducting, managing, and analyzing research workflows in natural hazards engineering. It brings together **interactive computing environments**, **shared data services**, and **large-scale computational resources** to support the full research lifecycle — from early model development, to large ensemble simulations, to advanced post-processing and data analysis.

At its core, DesignSafe is tightly integrated with the **Texas Advanced Computing Center (TACC)**, which supplies the high-performance computing (HPC) systems and large-scale storage needed to execute demanding analyses. Most computational jobs launched through DesignSafe — whether from the web portal, a Jupyter notebook, or an automated pipeline — ultimately run on TACC systems such as **Stampede3**, enabling simulations and studies that would be impractical or impossible on local machines.

DesignSafe is designed with **flexibility and scalability** in mind. The same platform supports lightweight, interactive exploration as well as production-scale simulations spanning many nodes and thousands of CPU cores. Understanding how to move effectively between these modes — and how the underlying system supports them — is essential for building efficient and reproducible research workflows.

***This document focuses on that understanding:*** Rather than centering on a specific application, it introduces the *computational architecture and workflow concepts* that underpin research computing on DesignSafe. These concepts apply broadly across tools, disciplines, and use cases, and they form the foundation for the application-specific examples presented in companion documents.



---
  
:::{include} TAILS.md
:::