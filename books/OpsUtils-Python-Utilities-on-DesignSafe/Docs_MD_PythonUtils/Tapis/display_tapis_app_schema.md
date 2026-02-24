# display_tapis_app_schema()
***display_tapis_app_schema(thisAppSchema)***

Pretty-prints a **Tapis App schema** (or any nested **TapisResult/dict/list**) in a clean, JSON-like format. Keys are grouped for readability—**scalars first**, then **lists**, then **nested dicts**—and TapisResult objects are seamlessly expanded via their internal attributes.

## What it does

* Accepts a Tapis App schema returned by *tapipy* (or a plain *dict*/*list*).
* Unwraps *TapisResult* values into dictionaries automatically.
* Prints arrays inline if they contain simple values, or **expands them** if they contain objects.
* Displays a neat **header** with *appID* and *version* when available.

## Signature

```python
display_tapis_app_schema(thisAppSchema)
```

## Parameters

* *thisAppSchema* *(TapisResult | dict | list)* — The schema or nested object to display.

## Returns

* *None* — The function prints to stdout.

## Example

```python
# Suppose you fetched an app with tapipy:
app_schema = t.apps.getApp(appId="opensees-mp-s3", appVersion="latest")

# Print a readable schema view
display_tapis_app_schema(app_schema)
```

**Sample output (excerpt):**

```
########################################
########### TAPIS-APP SCHEMA ###########
########################################
######## appID: opensees-mp-s3
######## version: latest
########################################
root: {
  id: "opensees-mp-s3"
  version: "latest"
  name: "OpenSeesMP on Stampede3"
  inputs: [
    {
      id: "input_dir"
      required: true
      description: "Directory with input files"
    }
    ...
  ]
  ...
}
########################################
```
---

#### Files

You can find these files in Community Data.

```{dropdown} display_tapis_app_schema.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Tapis/display_tapis_app_schema.py
:language: none
```
