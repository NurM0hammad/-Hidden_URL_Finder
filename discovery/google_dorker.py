from urllib.parse import urlsplit
def build_passive_search_queries(target):
    host = urlsplit(target).hostname
    if not host: return []
    return [f"site:{host}", f"site:{host} filetype:pdf", f"site:{host} inurl:api",
            f"site:{host} inurl:docs", f"site:{host} ext:json"]
