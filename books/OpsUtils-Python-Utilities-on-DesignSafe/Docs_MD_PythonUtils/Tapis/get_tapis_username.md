# get_tapis_username()
***get_tapis_username(t,*,prefer_userinfo: bool = True,fallback_to_token: bool = True,default=None,verbose: bool = False)***

**Purpose:** Robustly determine the **Tapis username** from an authenticated *tapipy.tapis.Tapis* client, even in environments where certain endpoints are restricted.

### What it does

* **Primary**: calls *t.authenticator.get_userinfo()* and returns *.username*.
* **Fallbacks** (no crashes):

  1. *t.username* attribute (if set by the client).
  2. Access token **claims**:

     * *t.access_token.claims["tapis/username"]* (or *"username"*)
     * *t.tokens.validateToken()["tapis/username"]* as a last resort.
* Returns *default* if none of the above yield a username.

### Signature

```python
get_tapis_username(
    t,
    *,
    prefer_userinfo: bool = True,
    fallback_to_token: bool = True,
    default=None,
    verbose: bool = False,
) -> str | Any
```

### Parameters

* **t** (*tapipy.tapis.Tapis*): Authenticated client.
* **prefer\_userinfo** (*bool, default True*): Try the userinfo endpoint first.
* **fallback\_to\_token** (*bool, default True*): Use token claims if userinfo is unavailable.
* **default** (*Any, default None*): Value returned when no username can be found.
* **verbose** (*bool, default False*): Print short diagnostics while resolving.

### Returns

* **str** — the resolved username (e.g., *"silvia"*), or
* ***default*** — if no method could determine the username.

### Examples

```python
# Basic
user = get_tapis_username(t)
print("Tapis username:", user or "(unknown)")

# Verbose troubleshooting and strict check
user = get_tapis_username(t, verbose=True)
if user is None:
    raise RuntimeError("Could not determine Tapis username from userinfo, client, or token claims.")
```

### Notes & tips

* In some **managed hubs** or service-token contexts, *get_userinfo()* may be disabled; token claims are usually available and are safe to use for identifying the caller.
* If you need both the **tenant** and username for logging, you can also read *t.access_token.claims["tapis/tenant_id"]* when available.
* Avoid caching the result for long-running jobs if you rotate tokens mid-session.


#### Files
You can find these files in Community Data.

```{dropdown} get_tapis_username.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Tapis/get_tapis_username.py
:language: none
```

