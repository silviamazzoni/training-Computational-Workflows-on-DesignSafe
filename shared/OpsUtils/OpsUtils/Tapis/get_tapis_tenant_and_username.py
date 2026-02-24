def get_tapis_tenant_and_username(
    t,
    *,
    prefer_userinfo: bool = True,
    fallback_to_token: bool = True,
    default_tenant=None,
    default_username=None,
    verbose: bool = False,
):
    """
    Return (tenant_id, username) from an authenticated Tapis client `t`,
    with safe fallbacks and no hard failures.

    Resolution order
    ----------------
    username:
      1) userinfo: t.authenticator.get_userinfo().username  (if prefer_userinfo)
      2) client attribute: getattr(t, "username", None)
      3) token claims / validation (if fallback_to_token):
         - t.access_token.claims["tapis/username"] or ["username"]
         - t.tokens.validateToken()["tapis/username"] (last resort)

    tenant_id:
      1) token claims: t.access_token.claims["tapis/tenant_id"] or ["tenant_id"]
      2) tokens.validateToken()["tapis/tenant_id"] (last resort, if fallback_to_token)
      3) userinfo dict fields (best-effort): ["tapis/tenant_id"] or ["tenant_id"] (if prefer_userinfo)
      4) getattr(t, "tenant_id", None)  (not standard, but handled if present)

    Parameters
    ----------
    t : tapipy.tapis.Tapis
        Authenticated Tapis client.
    prefer_userinfo : bool, default True
        Try the userinfo endpoint first when resolving the username (and, as a
        best-effort, tenant). Some hubs disable this; the function will fall back.
    fallback_to_token : bool, default True
        Allow reading tenant/username from token claims or validateToken().
    default_tenant : Any, default None
        Value returned if tenant cannot be determined.
    default_username : Any, default None
        Value returned if username cannot be determined.
    verbose : bool, default False
        Print short diagnostics while attempting fallbacks.

    Returns
    -------
    tuple
        (tenant_id, username) — strings when available, otherwise the provided defaults.

    Notes
    -----
    - Token claims are the most reliable source for the tenant in multi-tenant deployments.
    - Avoid trying to infer the tenant from base_url; many tenants share the same host.

    Examples
    --------
    >>> tenant, user = get_tenant_and_username(t)
    >>> print(f"Context: tenant={tenant}, user={user}")
    """
    # --- helpers
    def _claims():
        try:
            return getattr(getattr(t, "access_token", None), "claims", None)
        except Exception:
            return None

    def _from_claims(keys):
        c = _claims()
        if isinstance(c, dict):
            for k in keys:
                val = c.get(k)
                if val:
                    return val
        return None

    # --- username
    username = None
    if prefer_userinfo:
        try:
            ui = t.authenticator.get_userinfo()
            username = getattr(ui, "username", None)
            if not username and isinstance(ui, dict):
                username = ui.get("username")
            if not username and verbose:
                print("userinfo had no 'username'; will fall back…")
        except Exception as e:
            if verbose:
                print(f"userinfo unavailable for username: {e}")

    if not username:
        try:
            username = getattr(t, "username", None)
        except Exception:
            username = None

    if not username and fallback_to_token:
        username = _from_claims(["tapis/username", "username"])
        if not username:
            try:
                tok = t.tokens.validateToken()
                if isinstance(tok, dict):
                    username = tok.get("tapis/username") or tok.get("username")
            except Exception as e:
                if verbose:
                    print(f"tokens.validateToken (username) failed: {e}")

    if not username:
        username = default_username

    # --- tenant_id
    tenant = _from_claims(["tapis/tenant_id", "tenant_id"])
    if not tenant and fallback_to_token:
        try:
            tok = t.tokens.validateToken()
            if isinstance(tok, dict):
                tenant = tok.get("tapis/tenant_id") or tok.get("tenant_id")
        except Exception as e:
            if verbose:
                print(f"tokens.validateToken (tenant) failed: {e}")

    if not tenant and prefer_userinfo:
        try:
            ui = t.authenticator.get_userinfo()
            if isinstance(ui, dict):
                tenant = ui.get("tapis/tenant_id") or ui.get("tenant_id")
        except Exception:
            pass

    if not tenant:
        # non-standard, but some clients stash it
        tenant = getattr(t, "tenant_id", None)

    if not tenant:
        tenant = default_tenant

    return tenant, username
