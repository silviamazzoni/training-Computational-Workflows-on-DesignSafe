# Upload File to Tapis
***Example: Uploading a File to a Tapis Storage System***

Here's how you can **upload a file to a Tapis storage system** using **Tapipy**. This is often the first step before running a job, especially if your input files aren't already on the system.


1. **Connect and Authenticate** (if you haven’t already)

```python
from tapipy.tapis import Tapis

client = Tapis(base_url="https://<your-tapis-api-url>",
               username="<your-username>",
               password="<your-password>",
               tenant_id="<your-tenant-id>")

client.get_tokens()
```


2. **Upload the File**
    
    You’ll need:
    
    * The **ID of the storage system** (e.g., your user storage or a community system)
    * The **path** on that system where you want to upload the file
    * The **local file path** of the file you’re uploading
    
    ```python
    # Example values
    storage_system_id = "my-storage-system"
    remote_path = "input_files/my_data.txt"        # Path on Tapis system
    local_file_path = "my_data.txt"                # Local file
    
    # Open and upload the file
    with open(local_file_path, "rb") as file_stream:
        client.files.insert(
            systemId=storage_system_id,
            path=remote_path,
            file=file_stream
        )
    
    print(f"File '{local_file_path}' uploaded to '{storage_system_id}:{remote_path}'")
    ```
    
    This makes the file available for any Tapis app or job to use as input.


```{admonition} Pro Tip: List Files in a Remote Directory

    Want to confirm the upload or see what’s in a remote folder?
    
    ```python
    files = client.files.listFiles(systemId=storage_system_id, path="input_files")
    for f in files:
        print(f.name, f.type)
    ```
    
    ---
    
    Once the file is uploaded, you can reference it in your job submission like this:
    
    ```python
    "inputs": {
        "input_file": f"tapis://{storage_system_id}/input_files/my_data.txt"
    }
    ```
```