from bs4 import BeautifulSoup
from urllib.parse import urljoin
def analyze_html(html, page_url, guard):
    soup = BeautifulSoup(html or "", "html.parser")
    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    links = set()
    for tag in soup.find_all("a", href=True):
        try: links.add(guard.check(urljoin(page_url, tag["href"])))
        except Exception: pass
    forms = [{"method": (f.get("method") or "get").lower(), "action": f.get("action","")[:300]} for f in soup.find_all("form")]
    return {"title": title[:300], "links": sorted(links), "forms": forms}
