def bump_app_version(version: str, part: str = "patch", reset_trailing: bool = True) -> str:
    """
    Bump a 3-part version string "X.Y.Z" by the chosen part.

    Args:
        version: Version like "0.0.7" (digits only, three parts).
        part: Which number to bump: "major", "minor", or "patch" (default "patch").
        reset_trailing: If True, reset trailing numbers to 0 (SemVer-style). Default True.

    Returns:
        New version string.

    Examples:
        bump_version("0.0.7")                       -> "0.0.8"
        bump_version("0.0.7", part="minor")         -> "0.1.0"
        bump_version("1.2.3", part="major")         -> "2.0.0"
        bump_version("1.2.3", part="minor", reset_trailing=False) -> "1.3.3"

    Author: Silvia Mazzoni, DesignSafe (silviamazzoni@yahoo.com)
    """
    import re

    m = re.fullmatch(r"\s*(\d+)\.(\d+)\.(\d+)\s*", version)
    if not m:
        raise ValueError(f"Invalid version '{version}'. Expected 'X.Y.Z' with digits only.")

    major, minor, patch = (int(m.group(1)), int(m.group(2)), int(m.group(3)))
    print('Update type:',part)

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