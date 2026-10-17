from config import load_config, OUTPUT_DIR, WORDLIST_FILE
from logger import setup_logger
from scope_guard import ScopeGuard
from discovery.brute_forcer import discover_paths
from discovery.wayback_miner import mine_wayback
from discovery.js_extractor import extract_js_urls, extract_endpoints
from discovery.robots_parser import discover_robots_sitemap
from discovery.google_dorker import build_passive_search_queries
from discovery.response_differ import classify_response
from analyzers.content_analyzer import analyze_html
from analyzers.secrets_scanner import scan_text
from reporters.report_generator import write_reports
import requests

def main():
    cfg = load_config(); guard = ScopeGuard(cfg); target = guard.check(cfg["target"])
    logger = setup_logger(OUTPUT_DIR); timeout = int(cfg["request_timeout_seconds"])
    session = requests.Session(); session.headers.update({"User-Agent":cfg["user_agent"]})
    urls = {}; secret_findings = []
    def add(url, source, status=""):
        try:
            checked = guard.check(url)
            urls.setdefault(checked, {"url":checked, "source":source, "status":status})
        except Exception: pass

    logger.info("Starting scoped discovery: %s", target)
    for u in mine_wayback(target, guard, cfg["max_wayback_results"], timeout, logger): add(u,"wayback")
    for u in discover_robots_sitemap(target, guard, timeout, logger): add(u,"robots_or_sitemap")
    try:
        response = session.get(target, timeout=timeout, allow_redirects=False)
        add(target,"landing_page",str(response.status_code))
        if response.status_code == 200 and "text/html" in response.headers.get("Content-Type",""):
            secret_findings = scan_text(response.text)
            info = analyze_html(response.text,target,guard)
            for u in info["links"]: add(u,"html_link")
            for js in extract_js_urls(response.text,target,guard,cfg["max_js_files"]):
                add(js,"javascript_file")
                try:
                    jr = session.get(js,timeout=timeout,allow_redirects=False)
                    if jr.status_code == 200:
                        for u in extract_endpoints(jr.text,js,guard): add(u,"javascript_endpoint")
                except Exception as exc: logger.warning("JS fetch failed: %s",type(exc).__name__)
    except Exception as exc: logger.warning("Landing-page fetch failed: %s",type(exc).__name__)

    words = WORDLIST_FILE.read_text(encoding="utf-8").splitlines()
    for item in discover_paths(session,target,guard,words,delay=cfg["request_delay_seconds"],
                               max_requests=cfg["max_requests"],timeout=timeout,logger=logger):
        add(item["url"],item["source"],str(item["status"]))
    queries = build_passive_search_queries(target)
    for q in queries: logger.info("Manual search query (not executed): %s",q)

    import time
    checked_count = 0
    for item in list(urls.values()):
        if item.get("status"): continue
        if checked_count >= int(cfg.get("max_pages", 100)):
            item["status"] = "not_checked"
            item["note"] = "max_pages_limit"
            continue
        try:
            r = session.get(item["url"],timeout=timeout,allow_redirects=False,stream=True)
            item["status"] = str(r.status_code)
            item["classification"] = classify_response(r.status_code,r.headers.get("Content-Type",""),"")
            r.close()
            checked_count += 1
        except Exception as exc:
            item["status"] = "not_checked"; item["note"] = type(exc).__name__
        time.sleep(max(0.5, float(cfg["request_delay_seconds"])))
    report = {"target":target,"scope":{"allowed_hosts":sorted(guard.allowed_hosts),
             "allow_subdomains":guard.allow_subdomains},
             "summary":{"unique_urls":len(urls),"redacted_pattern_findings":len(secret_findings)},
             "urls":sorted(urls.values(),key=lambda x:x["url"]),
             "redacted_pattern_findings":secret_findings,"manual_search_queries":queries,
             "notes":["Use only on owned/explicitly authorized systems.","Discovered URLs are candidates, not vulnerabilities.",
                      "Redirects are not followed; out-of-scope hosts are rejected.",
                      "Secret matches are redacted and may be false positives."]}
    jp,hp = write_reports(OUTPUT_DIR,report)
    logger.info("Done. %d unique URLs. Reports: %s ; %s",len(urls),jp,hp)
if __name__ == "__main__": main()
