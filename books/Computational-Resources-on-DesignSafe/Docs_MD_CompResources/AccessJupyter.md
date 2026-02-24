# Accessing JupyterHub
***Accessing JupyterHub on DesignSafe***

## Step 0: Log In to DesignSafe

To get started, visit [https://www.designsafe-ci.org](https://www.designsafe-ci.org) and log in using your DesignSafe account credentials.

>  **Note:** You do **not** need an HPC allocation to launch a JupyterHub session. These interactive sessions are available to all registered users.

## Step 1: Launch a JupyterHub Session

Once logged in:

1. Navigate to the **Tools & Applications** section from the main DesignSafe dashboard.
2. Select the **Jupyter** application from the list.
3. Review any relevant documentation and follow the on-screen instructions to launch your session.

On the **Jupyter Overview** page, you’ll see several options for launching different types of environments:

* **JupyterHub** – *Recommended for this training*
  This launches a containerized session inside a shared Kubernetes-managed environment. It provides up to **8 CPU cores** and **20 GB of RAM** and is ideal for developing, testing, and submitting OpenSees jobs.

* **Jupyter on HPC Nodes (CPU or GPU)** – *Not covered in this training*
  These options connect you directly to a compute node on Stampede, Frontera, or other TACC systems. They require an allocation and are subject to queuing delays. These are intended for workflows that require direct node access for specific software stacks.

## Step Last: Ending Your JupyterHub Session

* If you simply close your browser, your session will remain active in the background.
* To explicitly stop your session:

  1. Open the **File** menu in JupyterHub.
  2. Select **Hub Control Panel**.
  3. Click **Stop Server**.

>  **Recommendation:** Restart your session at least once per week or so to ensure you're using the latest software image and updates.
