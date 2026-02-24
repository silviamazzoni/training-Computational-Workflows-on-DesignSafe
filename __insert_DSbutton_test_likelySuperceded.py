import yaml
from pathlib import Path

import nbformat

from urllib.parse import quote

def insert_designsafe_button(notebook_path, position='top'):
    encoded = quote(f"CommunityData/OpenSees/TrainingMaterial/training-OpenSees-on-DesignSafe/{notebook_path}")
    base_url = f"https://jupyter.designsafe-ci.org/hub/user-redirect/notebooks/{encoded}"

    nb_path = Path(notebook_path)
    nb = nbformat.read(nb_path, as_version=4)

    # Construct relative path for the notebook link
    relative_path = nb_path.as_posix()
    designsafe_url = f"{base_url}/{relative_path}"

    # Create the markdown cell with button
    button_md = nbformat.v4.new_markdown_cell(f"""
<a href="{designsafe_url}" target="_blank">
    <button style="padding:8px 16px;font-size:16px;">🔗 Open in DesignSafe</button>
</a>
""")

    # Only insert if not already present
    existing_button = any(
        cell.cell_type == 'markdown' and 'Open in DesignSafe' in cell.source
        for cell in nb.cells[:2]  # Check first few cells
    )
    if not existing_button:
        if position == 'top':
            nb.cells.insert(0, button_md)
        elif position == 'bottom':
            nb.cells.append(button_md)

    nbformat.write(nb, nb_path)


noon = 'Jupyter_Notebooks/WebPortalSubmit/WebPortalSubmit_Arduino_Case1junk.ipynb'
insert_designsafe_button(noon,'top')