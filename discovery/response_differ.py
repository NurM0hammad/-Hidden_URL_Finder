def classify_response(status_code, content_type="", body=""):
    text = (body or "").lower()
    if status_code in (404,410): return "not_found"
    if status_code in (401,403): return "restricted"
    if status_code == 429: return "rate_limited"
    if status_code >= 500: return "server_error"
    if status_code == 200:
        if "text/html" in (content_type or "").lower() and any(x in text for x in ("page not found","404 not found","does not exist")):
            return "possible_soft_404"
        return "candidate"
    return "other"
