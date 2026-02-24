Here’s an updated, drop-in doc page that matches your current function’s behavior (including the “blank password lets you re-enter the username” flow and returning `None` when login is cancelled). I kept your structure and added the key nuances.

---

# connect\_tapis()

***connect\_tapis(token\_filePath="\~/.tapis\_tokens.json", base\_url="[https://designsafe.tapis.io](https://designsafe.tapis.io)", username="", password="", force\_connect=False)***

**Purpose.** Create an authenticated **Tapis** client (e.g., for DesignSafe) with **automatic token caching**. It reuses a valid saved token when available; otherwise it securely prompts for credentials, fetches a new token, saves it for next time, and returns a ready-to-use client.

---

### What it does

* **Checks** *token\_filePath* (default `~/.tapis_tokens.json`) for a saved token.
* **Valid token** → uses it directly (no login prompts).
* **Missing/expired** or **`force_connect=True`** → performs a fresh login, **saves** the token, and continues.
* **Prints** when the token expires and how long remains.
* **Interactive login behavior:**

  * If `username` argument is empty, you’ll be prompted for it (**blank = cancel**; returns `None`).
  * You’re then prompted for your password. **Press Enter on an empty password to restart the prompts and re-enter the username** (useful if you mistyped it).

---

### Parameters

* **token\_filePath** *(str, default `"~/.tapis_tokens.json"`)* – Path to the JSON token file.
* **base\_url** *(str, default `"https://designsafe.tapis.io"`)* – Tapis API base URL for your tenancy.
* **username** *(str, default `""`)* – Preset username; if empty, you’ll be prompted (blank cancels).
* **password** *(str, default `""`)* – Preset password; if empty, you’ll be prompted securely. **Blank at the prompt restarts** and lets you change the username.
* **force\_connect** *(bool, default `False`)* – Force a fresh login even if a valid token exists.

---

### Returns

* **Tapis client** (`tapipy.tapis.Tapis`) **or `None`**
  An authenticated client when successful; `None` if login was cancelled (blank username) or ultimately failed.

---

### Token file format (JSON)

```json
{
  "access_token": "…",
  "expires_at": "2025-08-31T12:34:56+00:00"
}
```

*Expiry strings are parsed leniently; naive timestamps are treated as UTC. On fresh login the file is saved and (best effort) chmod’ed to `0600`.*

---

### Examples

```python
# Use a saved token if valid; otherwise prompt and save a new one
t = connect_tapis()
if t:
    jobs = t.jobs.getJobList()
    for j in jobs:
        print(j.id, j.status)
```

Force a fresh login (rotate the token):

```python
t = connect_tapis(force_connect=True)
```

Provide credentials programmatically (no prompts on success):

```python
t = connect_tapis(username="me@example.org", password="********")
```

Custom token cache path (e.g., project workspace):

```python
t = connect_tapis(token_filePath="./.secrets/tapis_token.json")
```

Handle a cancelled login gracefully:

```python
t = connect_tapis()
if t is None:
    print("Login cancelled by user.")
```

Fix a mistyped username during prompts:

* At the **password** prompt, press **Enter** with a blank password → you’ll be re-prompted for the username and can try again.

---

### Notes & tips

* **Security:** The token file contains only the access token and expiry, not your password; the code attempts to set file permissions to `0600` after writing.
* **Portability:** You can point *token\_filePath* to a project-local location (e.g., inside a shared workspace) if appropriate.
* **Diagnostics:** On success you’ll see `-- AUTHENTICATED VIA SAVED TOKEN` (cache) or `-- AUTHENTICATED VIA FRESH LOGIN`. Expiry time and remaining duration are printed.

---

#### Files

You can find these files in Community Data.

````{dropdown} connect_tapis.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Tapis/connect_tapis.py
:language: none
````
