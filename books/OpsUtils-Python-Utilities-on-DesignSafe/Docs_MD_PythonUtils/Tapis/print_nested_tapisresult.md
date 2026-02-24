# print_nested_tapisresult()
***print_nested_tapisresult(obj, key0='obj.', indent=0)***

Pretty-prints a nested **TapisResult/dict/list** in a clean, JSON-like style. It unwraps TapisResult objects via their internal attributes, groups keys for readability (scalars → lists → dicts), and quotes strings so you can visually distinguish values.

## What it does

* Accepts **TapisResult**, **dict**, **list**, or scalars.
* Prints **scalars first**, then **lists**, then **nested dicts**.
* **Lists** print inline when simple, or **expanded** when containing objects/dicts.
* Strings are **quoted** to improve readability.
* Useful for inspecting **Tapis app schemas**, **job metadata**, and other responses.

## Signature

```python
print_nested_tapisresult(obj, key0='obj.', indent=0)
```

## Parameters

* *obj* *(TapisResult | dict | list | Any)* — The object to render.
* *key0* *(str, default *'obj.'*)* — Prefix for printed keys (handy for naming the root).
* *indent* *(int, default *0*)* — Indentation level (2 spaces per level).

## Returns

* *None* — Prints to stdout.

## Example

```python
schema = t.apps.getAppLatestVersion(appId="opensees-mp-s3")
print_nested_tapisresult(schema, key0="schema.")
```

---

#### Files
You can find these files in Community Data.

```{dropdown} print_nested_tapisresult.py
:icon: file-code
```{literalinclude} ../../../../shared/OpsUtils/OpsUtils/Tapis/print_nested_tapisresult.py
:language: none
```
