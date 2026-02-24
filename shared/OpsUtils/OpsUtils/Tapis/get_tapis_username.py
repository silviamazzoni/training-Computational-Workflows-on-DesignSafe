def get_tapis_username(
    t,
    *,
    prefer_userinfo: bool = True,
    fallback_to_token: bool = True,
    default=None,
    verbose: bool = False,
):
    """
    Return the Tapis username from an authenticated client `t`, with safe fallbacks.

    Resolution order (robust to Tapipy resource objects and dicts):
      1) userinfo endpoint (if available):
         t.authenticator.get_userinfo().username
      2) client attribute:
         getattr(t, "username", None)
      3) token claims (if fallback_to_token=True):
         - t.access_token.claims.get("tapis/username") or "username"
         - t.tokens.validateToken()["tapis/username"] (as a last resort)

    Parameters
    ----------
    t : tapipy.tapis.Tapis
        Authenticated Tapis client.
    prefer_userinfo : bool, default True
        Try `t.authenticator.get_userinfo()` first. Some managed hubs disable this;
        if it fails, the function silently falls back.
    fallback_to_token : bool, default True
        Allow using access-token claims or `validateToken()` as a fallback.
    default : Any, default None
        Value to return if no username can be determined.
    verbose : bool, default False
        If True, print brief hints when a resolution step fails.

    Returns
    -------
    str | Any
        The resolved username (e.g., "silvia"), or `default` if none found.

    Notes
    -----
    - Some deployments restrict the userinfo endpoint; token claims usually work.
    - If you always want a strict failure when username can't be found, set
      `default=None` (the default) and check for `None` at the call site.

    Examples
    --------
    >>> u = get_tapis_username(t)
    >>> if u is None:
    ...     raise RuntimeError("No Tapis username available")
    ... 
    >>> print("Running as:", u)
    """
    # 1) userinfo (preferred)
    if prefer_userinfo:
        try:
            ui = t.authenticator.get_userinfo()
            uname = getattr(ui, "username", None)
            if not uname and isinstance(ui, dict):
                uname = ui.get("username")
            if uname:
                return uname
            if verbose:
                print("userinfo returned no 'username'; falling back…")
        except Exception as e:
            if verbose:
                print(f"userinfo unavailable: {e}; falling back…")

    # 2) client attribute
    try:
        uname = getattr(t, "username", None)
        if uname:
            return uname
    except Exception:
        pass

    # 3) token claims (optional)
    if fallback_to_token:
        # 3a) direct claims on access_token (common in Tapipy)
        try:
            claims = getattr(getattr(t, "access_token", None), "claims", None)
            if isinstance(claims, dict):
                uname = claims.get("tapis/username") or claims.get("username")
                if uname:
                    return uname
        except Exception as e:
            if verbose:
                print(f"access_token.claims unavailable: {e}")

        # 3b) validateToken() call
        try:
            tok = t.tokens.validateToken()
            if isinstance(tok, dict):
                uname = tok.get("tapis/username") or tok.get("username")
                if uname:
                    return uname
        except Exception as e:
            if verbose:
                print(f"tokens.validateToken failed: {e}")

    # Nothing worked
    return default
