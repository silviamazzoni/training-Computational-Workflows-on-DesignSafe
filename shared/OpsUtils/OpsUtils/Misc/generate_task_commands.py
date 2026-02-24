from __future__ import annotations

from itertools import product
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence


import pandas as pd

def generate_task_commands(
    base_command: str,
    sweep: Mapping[str, Sequence[Any]],
    *,
    placeholder_style: str = "token",
) -> List[str]:
    """
    Expand a command template into a list of commands for all combinations.

    Parameters
    ----------
    base_command
        Command template containing placeholders for parameters. Example:

        'python3 -u simulate.py --alpha ALPHA --beta BETA --gamma GAMMA --output ".../slot_$LAUNCHER_TSK_ID"'

        Placeholders must match keys in `sweep`.

    sweep
        Mapping of placeholder -> list/tuple of values to sweep over.
        Example: {"ALPHA": [0.3, 0.5], "BETA": [1, 2]}

    placeholder_style
        How placeholders appear in `base_command`:
        - "token": placeholders are bare tokens like ALPHA, BETA (default)
        - "braces": placeholders are in braces like {ALPHA}, {BETA}

    Returns
    -------
    list of str
        One command per combination of values, in deterministic order based
        on the insertion order of `sweep`.

    Notes
    -----
    - This function does *string substitution only*; it does not validate that
      the command is runnable on your system.
    - Environment variables such as $WORK or $SLURM_JOB_ID are left untouched.
    """
    if not sweep:
        return [base_command]

    keys = list(sweep.keys())
    value_lists = [sweep[k] for k in keys]

    # Basic validation
    for k, vals in sweep.items():
        if not isinstance(vals, Sequence) or isinstance(vals, (str, bytes)):
            raise TypeError(f"sweep[{k!r}] must be a non-string sequence of values.")
        if len(vals) == 0:
            raise ValueError(f"sweep[{k!r}] is empty; provide at least one value.")

    commands: List[str] = []
    for combo in product(*value_lists):
        cmd = base_command
        for k, v in zip(keys, combo):
            if placeholder_style == "token":
                cmd = cmd.replace(k, str(v))
            elif placeholder_style == "braces":
                cmd = cmd.replace("{" + k + "}", str(v))
            else:
                raise ValueError("placeholder_style must be 'token' or 'braces'.")
        commands.append(cmd)

    return commands


def write_tasklist(commands: Iterable[str], outfile: str | Path) -> None:
    """
    Write commands to a PyLauncher tasklist file (one command per line).
    """
    outpath = Path(outfile)
    outpath.parent.mkdir(parents=True, exist_ok=True)
    outpath.write_text("\n".join(commands) + "\n", encoding="utf-8")

# # ---------------------------------------------------------------------
# # Example usage (edit these for your sweep)
# # ---------------------------------------------------------------------

# inputFilename = "simulate.py"

# base_command = (
#     f'python3 -u {inputFilename} '
#     f'--alpha ALPHA --beta BETA --gamma GAMMA '
#     f'--output "$WORK/sweep_$SLURM_JOB_ID/line_$LAUNCHER_JID/slot_$LAUNCHER_TSK_ID"'
# )

# # Define parameters for dynamic generation (add/remove keys freely)
# sweep_params: Dict[str, Sequence[Any]] = {
#     "ALPHA": [0.3, 0.5, 3.7],
#     "BETA": [1.1, 2, 3],
#     "GAMMA": ["a", "b", "c"],
# }

# generated_tasks = generate_task_commands(base_command, sweep_params, placeholder_style="token")

# print(f"Generated {len(generated_tasks)} task commands:")
# print("-" * 60)
# for cmd in generated_tasks:
#     print(cmd)

# # Optional: write a runsList file for PyLauncher
# # write_tasklist(generated_tasks, "runsList.txt")


def preview_sweep_table(sweep: Mapping[str, Sequence[Any]]) -> pd.DataFrame:
    """
    Create a preview table of all parameter combinations in a sweep.

    Parameters
    ----------
    sweep
        Mapping of parameter name -> sequence of values to sweep over.
        Example:
            {"ALPHA": [0.3, 0.5], "BETA": [1, 2], "GAMMA": ["a", "b"]}

    Returns
    -------
    pandas.DataFrame
        A table with one row per parameter combination. Column order follows
        the insertion order of `sweep`.

    Notes
    -----
    - This is intended for interactive notebooks. For large sweeps, consider
      displaying only `.head()` or sampling rows.
    - Numeric formatting (e.g., 3 significant figures) is handled by display
      settings; see example below.
    """
    if not sweep:
        return pd.DataFrame()

    keys = list(sweep.keys())
    value_lists = [sweep[k] for k in keys]

    # Basic validation
    for k, vals in sweep.items():
        if not isinstance(vals, Sequence) or isinstance(vals, (str, bytes)):
            raise TypeError(f"sweep[{k!r}] must be a non-string sequence of values.")
        if len(vals) == 0:
            raise ValueError(f"sweep[{k!r}] is empty; provide at least one value.")

    rows = [dict(zip(keys, combo)) for combo in product(*value_lists)]
    return pd.DataFrame(rows)

# # Example
# df = preview_sweep_table(sweep_params)
# print(f"Total runs: {len(df)}")
# df.head(10)

# # Optional: Display Numeric Values with 3 Significant Figures
# # If you want the notebook preview to show numbers with 3 significant figures, you can set a pandas display format:
# import pandas as pd
# pd.options.display.float_format = "{:.3g}".format
# df = preview_sweep_table(sweep_params)
# df

# # Tip for Large Sweeps
# # If your sweep is very large, preview only a small portion:
# df.sample(20, random_state=0)   # random sample of 20 rows
# # or
# df.head(20)                     # first 20 rows