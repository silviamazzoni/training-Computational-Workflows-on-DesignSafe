def interactive_tapis_job_explorer(t,JobsData_df):
    """
    Launches an interactive visual explorer for Tapis jobs in a Jupyter Notebook environment.

    This tool presents a rich, widget-based interface that allows users to:
    - Filter Tapis jobs by status, system, date range, and app ID.
    - Sort and browse available jobs, with optional full display.
    - Select a job and view its:
        • Metadata
        • Execution history
        • File outputs (with structure)
    - Download all output files or select and download/view individual outputs.
    
    The explorer dynamically updates available jobs and outputs based on filters,
    and provides a smooth, visual workflow for reviewing and managing simulation results.

    Parameters
    ----------
    t : Tapis
        An authenticated Tapis client instance (from `connect_tapis()`).

    JobsData_df : pandas.DataFrame
        A DataFrame containing job information with at least the following columns:
            - 'uuid' : Tapis job UUID
            - 'name' : job name
            - 'created' : job creation timestamp (UTC ISO format)
            - 'status' : job status string
            - 'execSystemId' : system the job ran on
            - 'appId' : ID of the application used

        Optional columns like 'index_column' can improve labeling of jobs.

    Notes
    -----
    - This tool is intended to be run in a Jupyter Notebook environment.
    - Uses `ipywidgets` for UI and assumes IPython display context.
    - Internally calls OpsUtils functions:
        • `connect_tapis()`
        • `get_tapis_job_metadata()`
        • `get_tapis_job_history()`
        • `process_tacc_job_history()`
        • `get_tapis_job_all_files()`

    Widgets and Features
    --------------------
    • Search Controls:
        - Filter jobs by creation date, status, execution system, and app ID
        - Sort jobs by any column; reverse sorting; show all rows

    • Selection & Metadata:
        - Dropdown menu to select a job
        - Displays job metadata, history, and job step durations

    • File Management:
        - Shows all output files (with optional download)
        - Individual file viewer for small text-based outputs
        - Bulk download option with overwrite toggle

    Returns
    -------
    None
        The function does not return data, but displays a widget-based interface in the notebook.

    Example
    -------
    >>> from TapisExplorer import interactive_tapis_job_explorer
    >>> t = OpsUtils.connect_tapis()
    >>> df = OpsUtils.get_jobs_dataframe(t)
    >>> interactive_tapis_job_explorer(t, df)
    """
    # Silvia Mazzoni, 2025

    import pandas as pd
    import ipywidgets as widgets
    # from datetime import datetime
    from IPython.display import display, clear_output
    import os
    from OpsUtils import OpsUtils

    if JobsData_df.empty:
        print("⚠️ No jobs found.")
        return

    if not 'created_dt' in JobsData_df.keys():
        JobsData_df['created_dt'] = pd.to_datetime(JobsData_df['created'], utc=True)

    connect_out = widgets.Output()
    display(connect_out)
    with connect_out:
        t=OpsUtils.connect_tapis()
    with connect_out:
        clear_output()
        
        
    JobsData_df_keys = list(JobsData_df.keys())
    # filtered = JobsData_df.copy()
    # -------------------------------
    #  Format widgets
    # -------------------------------
    borderedLayout=widgets.Layout(
        border='2px solid gray',
        padding='10px',
        margin='5px'
    )
    borderedLayoutRed=widgets.Layout(
        border='2px solid red',
        padding='10px',
        margin='5px'
    )
    # -------------------------------
    #  Build filter widgets
    # -------------------------------
    status_dropdown = widgets.Dropdown(
        options=['(any)'] + sorted(JobsData_df['status'].dropna().unique()),
        value='(any)',
        description='Status:',
        layout=widgets.Layout(width='50%'),
        style={'description_width': 'initial'},
        custom_id = 'status_dropdown'
    )
    execSystemId_dropdown = widgets.Dropdown(
        options=['(any)'] + sorted(JobsData_df['execSystemId'].dropna().unique()),
        value='(any)',
        description='Execution System:',
        layout=widgets.Layout(width='50%'),
        style={'description_width': 'initial'},
        custom_id = 'execSystemId_dropdown'
    )
    min_date = JobsData_df['created_dt'].min().date()
    max_date = JobsData_df['created_dt'].max().date()
    start_date_picker = widgets.DatePicker(
        description=f'Start Date ({min_date}-{max_date})', value=min_date,
        layout=widgets.Layout(width='50%'),
        style={'description_width': 'initial'},
        custom_id = 'start_date_picker'
    )
    end_date_picker = widgets.DatePicker(
        description=f'End Date ({min_date}-{max_date})', value=max_date,
        layout=widgets.Layout(width='50%'),
        style={'description_width': 'initial'},
        custom_id = 'end_date_picker'
    )

    app_dropdown = widgets.Dropdown(
        options=['(any)'] + sorted(JobsData_df['appId'].dropna().unique()),
        value='(any)',
        description='App ID:',
        layout=widgets.Layout(width='60%'),
        style={'description_width': 'initial'},
        custom_id = 'app_dropdown'
    )

    uuid_dropdown = widgets.Dropdown(
        options=[],
        description='Select Job:',
        layout=widgets.Layout(width='80%'),
        style={'description_width': 'initial'},
        custom_id = 'uuid_dropdown'
    )

    outputs_dropdown = widgets.Dropdown(
        options=[],
        description='Select Output:',
        layout=widgets.Layout(width='80%'),
        style={'description_width': 'initial'},
        custom_id = 'outputs_dropdown'
    )
    sorts_dropdown = widgets.Dropdown(
        options=JobsData_df_keys,
        value = 'created_dt',
        description='Sort Jobs By:',
        layout=widgets.Layout(width='80%'),
        style={'description_width': 'initial'},
        custom_id = 'sorts_dropdown'
    )
    # Checkbox to reverse order
    reverse_checkbox = widgets.Checkbox(
        value=False,
        description='Descending',
        custom_id = 'reverse_checkbox'
    )
    show_all_checkbox = widgets.Checkbox(
        value=False,
        description='Show all rows',
        custom_id = 'show_all_checkbox'
    )
    download_all_overwrite_checkbox = widgets.Checkbox(
        value=False,
        description='Overwrite',
        custom_id = 'download_all_overwrite_checkbox'
    )
    download_select_overwrite_checkbox = widgets.Checkbox(
        value=False,
        description='Overwrite',
        custom_id = 'download_select_overwrite_checkbox'
    )

    run_button = widgets.Button(description="Explore Selected Job", button_style='success')

    download_all_button = widgets.Button(description="Download All", button_style='info')
    viewfile_button = widgets.Button(description="View Selected", button_style='info')
    download_select_button = widgets.Button(description="Download Selected", button_style='info')

    # -------------------------------
    # Output boxes
    # -------------------------------
    ## search
    count_box = widgets.Output(layout=widgets.Layout(
        border='0px solid gray',
        padding='10px',
        margin='5px'
    ))
    ## jobs
    dataframe_box = widgets.Output()
    jobsWidget = widgets.VBox([
        widgets.HBox([sorts_dropdown,reverse_checkbox,show_all_checkbox],layout=widgets.Layout(width='75%')),
        dataframe_box
    ])
    jobs_accordion = widgets.Accordion(children=[jobsWidget])
    jobs_accordion.set_title(0, 'JOBS')
    
    main_search = widgets.VBox([
            widgets.Label(value='SEARCH PARAMETERS:'),
            widgets.HBox([start_date_picker, end_date_picker]),
            widgets.HBox([status_dropdown, execSystemId_dropdown, app_dropdown]),
            count_box,
            jobs_accordion
        ],layout=borderedLayout)


    ## select job
    run_button_status = widgets.Output()
    main_select =  widgets.VBox([
            widgets.Label(value='SELECT JOB:'),
            uuid_dropdown,
            widgets.Label(value='Options are update automatically as you change the search parameters.'),
            run_button,
            run_button_status
        ],layout=borderedLayout) 
    
    ## selected-job metadata
    metadata_box_base = widgets.Output()
    main_metadata =  widgets.VBox([
            # widgets.Label(value='SELECTED-JOB METADATA:'),
            metadata_box_base
        ])

    ## download all
    download_all_base = widgets.Output()
    main_download_all = widgets.VBox([
            # widgets.Label(value='DOWNLOAD ALL:'),
            download_all_base
        ])

    ## visualize & download individual files
    download_select_base = widgets.Output()
    main_download_select = widgets.VBox([
           # widgets.Label(value='VISUALIZE & DOWNLOAD INDIVIDUAL FILES:'),
            download_select_base
        ])


    ## combined all:
    main_box_in = widgets.VBox([
        widgets.HTML(value='<H3>JOB-SEARCH INPUT</H3>'),
        main_search,
        main_select,
    ],layout=borderedLayoutRed)
    
    main_box_out = widgets.VBox([
        widgets.HTML(value='<H3>SELECTED-JOB DATA</H3>'),
        main_metadata,
        main_download_all,
        main_download_select,
    ],layout=borderedLayoutRed)

    
    main_box_out_base = widgets.Output()
    main_box = widgets.VBox([
        widgets.HTML(value='<center><h2>-- EXPLORE TAPIS JOBS --</h2></center>'),
        main_box_in,
        main_box_out_base
    ])

    
    files_box = widgets.Output()
    
    metadata_selected_job = widgets.Output()
    
    # 
    outputs_box_metadata = widgets.Output()
    outputs_box_history = widgets.Output()
    outputs_box_historyPro = widgets.Output()
    
    outputs_box_contents = widgets.Output()
    # separate accordions so you can keep all open.
    metadata_accordion_metadata = widgets.Accordion(children=[outputs_box_metadata])
    metadata_accordion_metadata.set_title(0, 'Metadata')
    metadata_accordion_history = widgets.Accordion(children=[outputs_box_history])
    metadata_accordion_history.set_title(0, 'History')
    # metadata_accordion_Details = widgets.Accordion(children=[outputs_box_historyPro])
    # metadata_accordion_Details.set_title(0, 'Details')
    metadata_accordion_contents = widgets.Accordion(children=[outputs_box_contents])
    metadata_accordion_contents.set_title(0, 'Contents')

    # metadata_box = widgets.VBox([
    #     widgets.Label(value='SELECTED-JOB METADATA:'),
    #     metadata_selected_job,
    #     metadata_accordion_metadata,
    #     metadata_accordion_history,
    #     metadata_accordion_contents
    # ],layout=borderedLayout)

    metadata_box = widgets.VBox([
        widgets.Label(value='SELECTED-JOB METADATA:'),
        metadata_selected_job,
        outputs_box_metadata,
        outputs_box_history,
        outputs_box_contents
    ],layout=borderedLayout)

    outputs_box_files_ctrl = widgets.Output()
    outputs_box_files = widgets.Output()
    files_accordion = widgets.Accordion(children=[outputs_box_files])
    files_accordion.set_title(0, 'Files')


    download_all_out_base = widgets.Output()
    download_all_box = widgets.VBox([
        widgets.Label(value='DOWNLOAD ALL:'),
        widgets.HBox([download_all_button, download_all_overwrite_checkbox]),
        download_all_out_base
    ],layout=borderedLayout)


    download_select_out_base = widgets.Output()
    download_select_box = widgets.VBox([
        widgets.Label(value='VISUALIZE AND/OR DOWNLOAD SELECTED FILE:'),
        outputs_dropdown,
        widgets.HBox([download_select_button, download_select_overwrite_checkbox]),
        viewfile_button,
        download_select_out_base
    ],layout=borderedLayout)


    
    outputs_box = widgets.Output()
    with outputs_box:
        display(outputs_box_files_ctrl)
        display(files_accordion)


    # -------------------------------
    # Download logic
    # -------------------------------
    def on_viewfile_clicked(b):
        selected_path = outputs_dropdown.value
        view_select_out = widgets.Output()
        view_select_out_acc = widgets.Accordion(children=[view_select_out])
        view_select_out_acc.set_title(0, f" View: {selected_path}")
        view_select_out_acc.selected_index = 0
        with download_select_out_base:
            # clear_output()
            display(view_select_out_acc)
        with view_select_out:
            clear_output()
            
            if selected_path:
                local_file = selected_path.split('/')[-1]
                # print('selected_path',selected_path)
                jobUuid = uuid_dropdown.value
                data = t.jobs.getJobOutputDownload(jobUuid=jobUuid, outputPath=selected_path)
                print(f" Viewing: {selected_path}")
                textarea = widgets.Textarea(
                    value=data,
                    placeholder='',
                    description='',
                    disabled=False,
                    layout=widgets.Layout(width='100%', height='500px')
                )
                display(textarea)
            else:
                print(" No output file selected to download.")
    viewfile_button.on_click(on_viewfile_clicked)
    
    # -------------------------------
    # Download logic
    # -------------------------------
    def on_download_select_clicked(b):
        selected_path = outputs_dropdown.value
        overwrite = download_select_overwrite_checkbox.value
        download_select_out = widgets.Output()
        download_select_out_acc = widgets.Accordion(children=[download_select_out])
        download_select_out_acc.set_title(0, f'Download: {selected_path}')
        download_select_out_acc.selected_index = 0
        with download_select_out_base:
            # clear_output()
            display(download_select_out_acc)
        with download_select_out:
            clear_output()
            
            if selected_path:
                local_file = selected_path.split('/')[-1]
                homePath = os.path.expanduser('~')
                local_file = os.path.join(homePath, local_file)
                # print('local_file:',local_file)
                if os.path.exists(local_file) and not overwrite:
                    print(f"    [SKIP] {local_file} (already exists)")
                    return
                else:
                    jobUuid = uuid_dropdown.value
                    data = t.jobs.getJobOutputDownload(jobUuid=jobUuid, outputPath=selected_path)
                    with open(local_file, "wb") as f:
                        f.write(data)
                    print(f" Downloaded: {selected_path} to {local_file}")
            else:
                print(" No output file selected to download.")
    download_select_button.on_click(on_download_select_clicked)

    # -------------------------------
    # Download All logic
    # -------------------------------
    def on_download_all_clicked(b):
        overwrite = download_all_overwrite_checkbox.value
        download_all_out = widgets.Output()
        download_all_out_acc = widgets.Accordion(children=[download_all_out])
        download_all_out_acc.set_title(0, 'DOWNLOAD INFO')
        download_all_out_acc.selected_index = 0
        with download_all_out_base:
            clear_output()
            display(download_all_out_acc)
        
        
        with download_all_out:
            clear_output()
            jobUuid = uuid_dropdown.value
            returnedData = OpsUtils.get_tapis_job_all_files(t, jobUuid, displayIt=10, target_dir=f"outputs_{jobUuid}", overwrite=overwrite)
            print(f"File Download DONE!")
            
    download_all_button.on_click(on_download_all_clicked)

    

    # -------------------------------
    # Explore selected job
    # -------------------------------
    def explore_job(jobUuid):
        with run_button_status:
            clear_output()
            print('..... processing ....')

        with main_box_out_base:
            display(main_box_out)

        
        with outputs_box_files:
            clear_output()
            
        with metadata_selected_job:
            clear_output()
            print(f'*** JOB: {jobUuid} ***')
        
        with outputs_box_metadata:
            clear_output()
            OpsUtils.get_tapis_job_metadata(t, jobUuid)
            # get_tapis_job_history(t, jobUuid,print_all=False)
            # get_tapis_job_metadata(t, jobUuid)
        
       
        with outputs_box_history:
            clear_output()
            OpsUtils.get_tapis_job_history_data(t, jobUuid)       
       
        # with outputs_box_historyPro:
        #     clear_output()
        #     OpsUtils.get_tapis_job_history_durations(t, jobUuid,getMetadata=False)
        #     # process_tapis_job_history(t, jobUuid,getMetadata=False)



        with outputs_box_contents:
            clear_output()
            AllFilesDict = OpsUtils.get_tapis_job_all_files(t, jobUuid, displayIt=10, target_dir=False, overwrite=False)
            outputs_dropdown.options = []
            output_files = []
            for thisLocalPath in AllFilesDict['LocalPath']:
                output_files.append((thisLocalPath, thisLocalPath))
            if len(output_files)>0:
                outputs_dropdown.options = output_files
                outputs_dropdown.value = output_files[0][1]

        with download_all_base:
            clear_output()
            display(download_all_box)



        with download_select_base:
            clear_output()
            display(download_select_box)



        with metadata_box_base:
            clear_output()
            display(metadata_box)

        with run_button_status:
            clear_output()

    # -------------------------------
    #  Update jobs on filter change
    # -------------------------------
    def update_jobs(change):
        status_selected = status_dropdown.value
        execSystemId_selected = execSystemId_dropdown.value
        start = pd.to_datetime(start_date_picker.value).tz_localize('UTC')
        end = pd.to_datetime(end_date_picker.value).tz_localize('UTC')
        app_selected = app_dropdown.value

        filtered = JobsData_df[
            (JobsData_df['appId'] != 'opensees-interactive') &
            (JobsData_df['created_dt'] >= start) &
            (JobsData_df['created_dt'] <= end)
        ]
        if status_selected != '(any)':
            filtered = filtered[filtered['status'] == status_selected]
        if execSystemId_selected != '(any)':
            filtered = filtered[filtered['execSystemId'] == execSystemId_selected]
        if app_selected != '(any)':
            filtered = filtered[filtered['appId'] == app_selected]

        with count_box:
            clear_output()
            print(f" {len(filtered)} jobs found matching filters.")

        if filtered.empty:
            uuid_dropdown.options = []
            with outputs_box_history:
                clear_output()
                print(f" No jobs found matching these filters.")
        else:
            # Sort so latest job is first
            sort_selected = sorts_dropdown.value
            show_all_selected = show_all_checkbox.value
            filtered = filtered.sort_values(by=sort_selected, ascending=not reverse_checkbox.value)
            
            with dataframe_box:
                clear_output()
                if show_all_selected:
                    display(filtered.style.hide(axis="index"))
                else:
                    display(filtered.copy().reset_index(drop=True))
            job_options = [(f"{row['index_column']} | {row['name']} | {str(row['created_dt']).split('.')[0]} | {row['status']} | {row['appId']}  | {row['uuid'][:8]}...", row['uuid'])
                           for _, row in filtered.iterrows()] # | {row['execSystemId']}
            uuid_dropdown.options = job_options
            uuid_dropdown.value = job_options[0][1]  # auto-select most recent

    # -------------------------------
    #  Update jobs on filter change
    # -------------------------------
    def update_sorts(change):
        update_jobs(change)

        
    # Connect triggers
    status_dropdown.observe(update_jobs, names='value')
    execSystemId_dropdown.observe(update_jobs, names='value')
    start_date_picker.observe(update_jobs, names='value')
    end_date_picker.observe(update_jobs, names='value')
    app_dropdown.observe(update_jobs, names='value')

    sorts_dropdown.observe(update_sorts, names='value')
    reverse_checkbox.observe(update_sorts, names='value')
    show_all_checkbox.observe(update_sorts, names='value')

    
    run_button.on_click(lambda b: explore_job(uuid_dropdown.value))
    update_jobs(None)  # initial load

    display(main_box)

