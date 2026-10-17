from urllib.parse import urljoin
import time
def discover_paths(session, base_url, guard, wordlist, delay=1.0, max_requests=60, timeout=8, logger=None):
    found, count = [], 0
    base = guard.check(base_url).rstrip("/") + "/"
    for word in wordlist:
        word = word.strip().lstrip("/")
        if not word or word.startswith("#") or count >= max_requests: continue
        url = guard.check(urljoin(base, word))
        try:
            response = session.get(url, timeout=timeout, allow_redirects=False)
            count += 1
            if response.status_code not in (404, 410):
                found.append({"url": url, "status": response.status_code, "source": "limited_path_check"})
                if logger: logger.info("Path candidate: %s [%s]", url, response.status_code)
        except Exception as exc:
            if logger: logger.warning("Path check failed: %s", type(exc).__name__)
        time.sleep(max(0.5, float(delay)))
    return found
