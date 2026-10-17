from pathlib import Path
import yaml
BASE_DIR = Path(__file__).resolve().parent
SCOPE_FILE = BASE_DIR / "scope.yaml"
OUTPUT_DIR = BASE_DIR / "output"
WORDLIST_FILE = BASE_DIR / "wordlist.txt"
def load_config():
    with SCOPE_FILE.open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
    if not cfg.get("target") or not cfg.get("allowed_hosts"):
        raise ValueError("scope.yaml must define target and allowed_hosts")
    cfg.setdefault("allow_subdomains", False)
    cfg.setdefault("request_delay_seconds", 1.0)
    cfg.setdefault("request_timeout_seconds", 8)
    cfg.setdefault("max_requests", 60)
    cfg.setdefault("max_js_files", 20)
    cfg.setdefault("max_wayback_results", 100)
    cfg.setdefault("user_agent", "HiddenURLFinder/1.0")
    return cfg
