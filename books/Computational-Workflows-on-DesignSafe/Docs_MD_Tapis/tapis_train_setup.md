## Set up Tapis

Before submitting an OpenSees job through a Tapis App, there are a few key steps to set up your environment and credentials. These steps only need to be done once per session (and in some cases, only once ever), but they are essential for a smooth workflow.

1. **Authenticate with Tapis**
   You must first connect to Tapis using your DesignSafe account. Once authenticated, you can call Tapis commands from within JupyterHub or your terminal. The Tapis authentication tokens have a finite duration, so you will have to connect to Tapis often. I have developed a python function that helps you manage your tokens efficiently.

   * To learn more about Tapis and authentication: [Tapis Documentation: Authentication](https://tapis.readthedocs.io/en/latest/technical/authentication.html)

2. **Choose and Check Your System**
   After authentication, confirm which HPC system you will be using—most likely **Stampede3**. It is helpful to review the system specifications (queues, node types, memory) so you know what resources are available for your job. The *t.systems.getSystem(systemId=system_id)* command returns some technical details about the nodes on your system. This information can be useful when setting up your job.

3. **Establish TMS Credentials**
   The **Tapis Tokens Management Service (TMS)** securely stores your credentials on the execution system of your choice (e.g. stampede3). You need to set this up once so that Tapis can manage job submissions and file transfers on your behalf.

4. **Work with Tapis Paths**
   Tapis uses storage paths that can be **user-** or **system-** **dependent**. To make things easier, we provide a notebook that explains how to construct and use these paths. You can also run a helper script that saves your account information to a file, reducing the chance of errors in future runs.

Taking time to set up these prerequisites ensures that when you submit a Tapis App, it will connect seamlessly to Stampede3, find your files, and return results to the correct location.

 [Tapis Documentation](https://tapis.readthedocs.io/en/latest)