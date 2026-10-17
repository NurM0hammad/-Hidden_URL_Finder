import requests
from urllib.parse import urlsplit
def mine_wayback(target, guard, limit=100, timeout=10, logger=None):
    host = urlsplit(guard.check(target)).hostname
    params = {"url": f"{host}/*", "output": "json", "fl": "original", "filter": "statuscode:200",
              "collapse": "urlkey", "limit": str(max(1, min(int(limit), 500)))}
    try:
        r = requests.get("https://web.archive.org/cdx/search/cdx", params=params, timeout=timeout,
                         headers={"User-Agent": "HiddenURLFinder/1.0"})
        r.raise_for_status()
        rows, results = r.json(), []
        for row in rows[1:] if rows else []:
            if isinstance(row, list) and row:
                try: results.append(guard.check(row[0]))
                except Exception: pass
        return sorted(set(results))
    except Exception as exc:
        if logger: logger.warning("Wayback lookup unavailable: %s", type(exc).__name__)
        return []
