# bump_app_version()
***Increment a Semantic Version String***

**Author:** Silvia Mazzoni, DesignSafe ([silviamazzoni@yahoo.com](mailto:silviamazzoni@yahoo.com))
**Purpose:** Compute the next version string by bumping one component of a *X.Y.Z* semantic-style version.

---

## Signature

'''python
def bump_app_version(version: str,
                     part: str = "patch",
                     reset_trailing: bool = True) -> str:
'''

## Parameters

* ***version*** (*str*): A three-part, dot-separated numeric version like *"0.0.7"*.

  * Leading/trailing whitespace is allowed and ignored.
  * Each part must be digits only (no pre-release/build tags).

* ***part*** (*str*, default *"patch"*): Which component to bump.

  * *"major"*: increments *X*.
  * *"minor"*: increments *Y*.
  * *"patch"*: increments *Z*.

* ***reset_trailing*** (*bool*, default *True*): Whether to reset lower-order components to *0* after the bump (SemVer-style).

  * If *True*:

    * bump **major**: *X.Y.Z* → *(X+1).0.0*
    * bump **minor**: *X.Y.Z* → *X.(Y+1).0*
    * bump **patch**: *X.Y.Z* → *X.Y.(Z+1)* (no lower component to reset)
  * If *False*, only the chosen component is incremented and others are left as-is.

## Returns

* ***str***: The new version string in *X.Y.Z* format.

## Raises

* ***ValueError***: If *version* is not strictly *X.Y.Z* with numeric parts.
* ***ValueError***: If *part* is not one of *"major"*, *"minor"*, *"patch"*.

---

## Examples

'''python
bump_app_version("0.0.7")                         # -> "0.0.8"
bump_app_version("0.0.7", part="minor")           # -> "0.1.0"
bump_app_version("1.2.3", part="major")           # -> "2.0.0"
bump_app_version("1.2.3", part="minor", reset_trailing=False)
# -> "1.3.3"
'''

### Whitespace-tolerant

'''python
bump_app_version("  3.9.9  ", part="patch")       # -> "3.9.10"
'''

### Invalid inputs (raise *ValueError*)

```python
bump_app_version("1.2")        # not X.Y.Z
bump_app_version("1.2.beta")   # non-numeric
bump_app_version("v1.2.3")     # prefix not allowed
bump_app_version("1.2.3", part="build")  # unknown part
```

---

## Implementation (for reference)

```python
def bump_app_version(version: str, part: str = "patch", reset_trailing: bool = True) -> str:
    """
    Bump a 3-part version string "X.Y.Z" by the chosen part.

    Author: Silvia Mazzoni, DesignSafe (silviamazzoni@yahoo.com)
    """
    import re

    m = re.fullmatch(r"\s*(\d+)\.(\d+)\.(\d+)\s*", version)
    if not m:
        raise ValueError(f"Invalid version '{version}'. Expected 'X.Y.Z' with digits only.")

    major, minor, patch = (int(m.group(1)), int(m.group(2)), int(m.group(3)))

    if part == "major":
        major += 1
        if reset_trailing:
            minor, patch = 0, 0
    elif part == "minor":
        minor += 1
        if reset_trailing:
            patch = 0
    elif part == "patch":
        patch += 1
    else:
        raise ValueError("part must be one of: 'major', 'minor', 'patch'")

    return f"{major}.{minor}.{patch}"
```

---

## Notes & Best Practices

* **Strict numeric SemVer**: This helper intentionally **does not** parse pre-release or build metadata (e.g., *1.2.3-alpha+build*). If you need that, consider storing a pure numeric base separately or extending the regex/logic.
* **Determinism**: Given the same inputs, the function is pure and side-effect free, which makes it easy to unit test and integrate into CI/CD bumps.
* **Reset policy**: Keep *reset_trailing=True* for conventional SemVer behavior when bumping *major* or *minor*. Use *False* only if you deliberately want to preserve lower components.

---

## Minimal Tests (pytest)

```python
import pytest

def test_patch():
    assert bump_app_version("0.0.7") == "0.0.8"

def test_minor_reset():
    assert bump_app_version("1.2.9", part="minor") == "1.3.0"

def test_major_reset():
    assert bump_app_version("9.9.9", part="major") == "10.0.0"

def test_minor_no_reset():
    assert bump_app_version("1.2.3", part="minor", reset_trailing=False) == "1.3.3"

def test_whitespace():
    assert bump_app_version(" 2.0.9 ", part="patch") == "2.0.10"

@pytest.mark.parametrize("bad", ["1.2", "1.2.beta", "v1.2.3", "1.2.3.4"])
def test_invalid(bad):
    with pytest.raises(ValueError):
        bump_app_version(bad)

def test_bad_part():
    with pytest.raises(ValueError):
        bump_app_version("1.2.3", part="build")
```

---

## Typical Integration

* **Manual bump in scripts**: use directly before tagging/building.
* **CI/CD**: read current version (e.g., from a file), call *bump_app_version*, write back the new version, and proceed with packaging/release steps.
* **Tapis apps**: if you store versions as pure *X.Y.Z* strings, this function can generate the next version before registering a new app definition.
