from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser
import requests, re
def discover_robots_sitemap(target, guard, timeout=8, logger=None):
    base = guard.check(target).rstrip("/")
    robots_url = guard.check(base + "/robots.txt")
    results = set()
    try:
        r = requests.get(robots_url, timeout=timeout, allow_redirects=False, headers={"User-Agent":"HiddenURLFinder/1.0"})
        if r.status_code == 200:
            parser = RobotFileParser(); parser.set_url(robots_url); parser.parse(r.text.splitlines())
            for line in r.text.splitlines():
                if line.strip().lower().startswith("sitemap:"):
                    try: results.add(guard.check(line.split(":",1)[1].strip()))
                    except Exception: pass
            for entry in parser.entries:
                for path in entry.allow + entry.disallow:
                    if path and "*" not in path and "$" not in path:
                        try: results.add(guard.check(urljoin(base + "/", path.lstrip("/"))))
                        except Exception: pass
    except Exception as exc:
        if logger: logger.warning("robots lookup failed: %s", type(exc).__name__)
    for candidate in list(results)[:10]:
        if "sitemap" not in candidate.lower(): continue
        try:
            r = requests.get(candidate, timeout=timeout, allow_redirects=False, headers={"User-Agent":"HiddenURLFinder/1.0"})
            if r.status_code == 200:
                for loc in re.findall(r"<loc>\s*(.*?)\s*</loc>", r.text, re.I|re.S):
                    try: results.add(guard.check(loc.strip()))
                    except Exception: pass
        except Exception: pass
    return sorted(results)
