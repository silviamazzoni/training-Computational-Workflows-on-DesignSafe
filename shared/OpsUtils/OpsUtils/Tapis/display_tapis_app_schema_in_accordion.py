def display_tapis_app_schema_in_accordion(t, appId: str, appVersion: str = "latest",jobInputOnly:bool = True,useAccordion:bool=True):
    """
    Pretty-print a Tapis App schema in a
    JSON-like format with readable grouping and indentation inside an accordion

    Behavior
    --------
    - Accepts a TapisResult, dict, or list.
    - Groups and prints keys in the order: scalars → lists → nested dicts.
    - Handles TapisResult values by flattening their internal __dict__.
    - Prints arrays either inline (simple scalars) or expanded (objects).
    - Shows a header with app id and version (if present).

    Parameters
    ----------
    thisAppSchema : tapipy.tapis.TapisResult | dict | list
        The app schema or object to render.

    Returns
    -------
    None
        This function prints to stdout. It does not return a value.

    Example
    -------
    # Given a Tapis app schema returned by tapipy:
    display_tapis_app_schema(app_schema)

    Author
    ------
    Silvia Mazzoni, DesignSafe (silviamazzoni@yahoo.com)

    Date
    ----
    2025-08-14

    Version
    -------
    1.0
    """



    ## -- get_tapis_app_schema --
    from tapipy.errors import BaseTapyException

    # Normalize appVersion
    appVersion = (appVersion or "").strip().lower()

    try:
        if appVersion == "" or appVersion == "latest":
            thisAppSchema = t.apps.getAppLatestVersion(appId=appId)
        else:
            thisAppSchema =  t.apps.getApp(appId=appId, appVersion=appVersion)
    except BaseTapyException as e:
        if not quiet:
            print(f"I was unable to find Tapis app: '{appId}', appVersion='{appVersion}'. Error: {e}")
        return None
    except Exception as e:
        if not quiet:
            print(f"Unexpected error retrieving app '{appId}' (appVersion='{appVersion}'): {e}")
        return None

    
    ## -- display_tapis_app_schema
    try:
        from tapipy.tapis import TapisResult
    except Exception:
        class TapisResult:  # sentinel so isinstance checks won’t crash if tapipy not available
            pass

    def _is_simple_scalar(x):
        return isinstance(x, (type(None), bool, int, float, str))

    def _quote_if_str(x):
        return f'"{x}"' if isinstance(x, str) else x


    AppInputKeys = []
    HPCInputKeys = []
    AdvInputKeys = []
    def print_nested(key_prefix, obj, indent=1,jobInputOnly=False):
        sp = '  ' * indent

        # Unwrap TapisResult to dict
        if isinstance(obj, TapisResult):
            obj = obj.__dict__

        # Dict handling
        if isinstance(obj, dict):
            dict_keys, list_keys, scalar_keys = [], [], []
            for k, v in obj.items():
                v_unwrap = v.__dict__ if isinstance(v, TapisResult) else v
                if isinstance(v_unwrap, dict):
                    dict_keys.append(k)
                elif isinstance(v_unwrap, list):
                    list_keys.append(k)
                else:
                    scalar_keys.append(k)

            # print in order: scalars, lists, dicts
            ordered = [*scalar_keys, *list_keys, *dict_keys]
            for i, k in enumerate(ordered):
                if jobInputOnly:
                    if k in ['notes','isMpi','mpiCmd','dynamicExecSystem','execSystemConstraints','dtnSystemInputDir','dtnSystemOutputDir','archiveMode','cmdPrefix','tags']:
                        continue
                v = obj[k]
                if jobInputOnly:
                    if k in ['key','name']:
                        AppInputKeys.append(f'{v}')
                    if indent==1 and not isinstance(v, TapisResult) and not isinstance(v, list):
                        if k in ['execSystemLogicalQueue','nodeCount','coresPerNode','memoryMB','maxMinutes']:
                            HPCInputKeys.append(f'{k}')
                        else:
                            AdvInputKeys.append(f'{k} = {v}')
                v_unwrap = v.__dict__ if isinstance(v, TapisResult) else v
               
                # Nested dict or object
                if isinstance(v_unwrap, dict):
                    # opening brace for top-level objects
                    if key_prefix:
                        print(f'{sp}{key_prefix}{k}: ' + '{')
                        next_prefix = ""
                    else:
                        print(f'{sp}{k}: ' + '{')
                        next_prefix = ""
                    print_nested(next_prefix, v_unwrap, indent + 1,jobInputOnly=jobInputOnly)
                    print(f'{sp}' + '}')
                    if i != len(ordered) - 1:
                        pass  # stylistically omit commas for readability

                # Lists
                elif isinstance(v_unwrap, list):
                    # Decide inline vs expanded
                    contains_objects = any(
                        (isinstance(it, (dict, TapisResult))) for it in v_unwrap
                    )
                    label = f'{sp}{key_prefix}{k}: ' if key_prefix else f'{sp}{k}: '
                    if not v_unwrap:
                        print(label + '[]')
                    elif contains_objects:
                        print(label + '[')
                        for j, it in enumerate(v_unwrap):
                            it_unwrap = it.__dict__ if isinstance(it, TapisResult) else it
                            if isinstance(it_unwrap, dict):
                                print('  ' * (indent + 1) + '{')
                                print_nested("", it_unwrap, indent + 2,jobInputOnly=jobInputOnly)
                                print('  ' * (indent + 1) + '}')
                            else:
                                val = _quote_if_str(it_unwrap)
                                print('  ' * (indent + 1) + f'{val}')
                            if j != len(v_unwrap) - 1:
                                pass  # omit commas for readability
                        print(sp + ']')
                    else:
                        # all simple values → inline
                        vals = [_quote_if_str(x) for x in v_unwrap]
                        print(label + f'[{", ".join(map(str, vals))}]')

                # Scalars
                else:
                    val = _quote_if_str(v_unwrap)
                    label = f'{sp}{key_prefix}{k}: ' if key_prefix else f'{sp}{k}: '
                    print(label + f'{val}')

        # List handling (rare for top-level)
        elif isinstance(obj, list):
            sp = '  ' * indent
            if not obj:
                print(sp + '[]')
                return
            contains_objects = any(isinstance(it, (dict, TapisResult)) for it in obj)
            if contains_objects:
                print(sp + '[')
                for it in obj:
                    it_unwrap = it.__dict__ if isinstance(it, TapisResult) else it
                    if isinstance(it_unwrap, dict):
                        print('  ' * (indent + 1) + '{')
                        print_nested("", it_unwrap, indent + 2,jobInputOnly=jobInputOnly)
                        print('  ' * (indent + 1) + '}')
                    else:
                        print('  ' * (indent + 1) + f'{_quote_if_str(it_unwrap)}')
                print(sp + ']')
            else:
                vals = [_quote_if_str(x) for x in obj]
                print(sp + f'[{", ".join(map(str, vals))}]')

        # Fallback scalar
        else:
            val = _quote_if_str(obj)
            print(sp + f'{val}')
    


    def displayAllOutput(appId,appVersion,thisAppSchema):
        print('########################################')
        print('########### TAPIS-APP SCHEMA ###########')
        print('########################################')
        # Best-effort id/version extraction
        
        if appId is not None:
            print(f'######## appID: {appId}')
        if appVersion is not None:
            print(f'######## appVersion: {appVersion}')
        print('########################################')
        print('{')
        print_nested("", thisAppSchema, indent=1,jobInputOnly=False)
        print('}')    
        print('########################################')
        
    def displayJobInputOnly(appId,appVersion,thisAppSchema):
        print('****************************************')
        print('******** JOB ATTRIBUTES ONLY ***********')
        print('****************************************')
        print('{')
        print_nested("", thisAppSchema.jobAttributes, indent=1,jobInputOnly=True)
        print('}')
        print('****************************************')
        
    def displaySummaryJobInputOnly(appId,appVersion,thisAppSchema):
        print('++++++++++++++++++++++++++++++++++++++++')
        print('++++++++ SUMMARY: INPUT KEYS +++++++++++')
        print('++++++++++++++++++++++++++++++++++++++++')
        if len(HPCInputKeys)>0:
            print('-------------------------------')
            print('---- SLURM-control keys -------')
            print('-------------------------------')
            for thisKey in HPCInputKeys:
                print(thisKey)
        if len(AppInputKeys)>0:
            print('-------------------------------')
            print('---- APP-control keys ---------')
            print('-------------------------------')
            for thisKey in AppInputKeys:
                print(thisKey)
        if len(AdvInputKeys)>0:
            print('-------------------------------')
            print('---- Advanced-control keys ----')
            print('-------------------------------')
            for thisKey in AdvInputKeys:
                print(thisKey)
        print('++++++++++++++++++++++++++++++++++++++++')
    
    if useAccordion:
        from IPython.display import display, HTML,Markdown
        import ipywidgets as widgets

        accordionTitle = f'___appId:_{appId}___appVersion:_{appVersion}______-- FULL APP DESCRIPTION --'
        here_out = widgets.Output()
        here_accordion = widgets.Accordion(children=[here_out])
        # here_accordion.selected_index = 0
        here_accordion.set_title(0, accordionTitle)
        display(here_accordion)
        with here_out:
            displayAllOutput(appId,appVersion,thisAppSchema)

        if jobInputOnly:
            accordionTitle = f'___appId:_{appId}___appVersion:_{appVersion}______-- JOB INPUT ONLY --'
            here_out = widgets.Output()
            here_accordion = widgets.Accordion(children=[here_out])
            # here_accordion.selected_index = 0
            here_accordion.set_title(0, accordionTitle)
            display(here_accordion)
            with here_out:
                displayJobInputOnly(appId,appVersion,thisAppSchema)
    
            accordionTitle = f'___appId:_{appId}___appVersion:_{appVersion}______-- SUMMARY: INPUT KEYS --'
            here_out = widgets.Output()
            here_accordion = widgets.Accordion(children=[here_out])
            # here_accordion.selected_index = 0
            here_accordion.set_title(0, accordionTitle)
            display(here_accordion)
            with here_out:
                displaySummaryJobInputOnly(appId,appVersion,thisAppSchema)
    
    
    else:
        displayAllOutput(appId,appVersion,thisAppSchema)
