import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
URL_RE = re.compile(r'''(?i)(?:https?://[^\s"'<>\\]+|/(?:api|v[0-9]+|auth|admin|graphql|static|assets)?/?[^\s"'<>\\]*)''')
def extract_js_urls(html, page_url, guard, max_files=20):
    soup = BeautifulSoup(html, "html.parser"); urls = set()
    for tag in soup.find_all("script", src=True):
        try: urls.add(guard.check(urljoin(page_url, tag["src"])))
        except Exception: pass
        if len(urls) >= max_files: break
    return sorted(urls)
def extract_endpoints(js_text, js_url, guard, limit=300):
    found = set()
    for match in URL_RE.findall(js_text or ""):
        try: found.add(guard.check(urljoin(js_url, match.rstrip(").,;"))))
        except Exception: pass
        if len(found) >= limit: break
    return sorted(found)
