# Hidden URL Finder

Conservative URL inventory tool for websites you own or are explicitly authorized to assess.

## Install

Windows 11 PowerShell:
```powershell
cd hidden-url-finder
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Kali Linux:
```bash
cd hidden-url-finder
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Configure and run
Edit `scope.yaml`: replace `https://example.com` and list only explicitly authorized hosts. Keep `allow_subdomains: false` unless permission covers subdomains. Then run:
```bash
python main.py
```
Reports: `output/report.json`, `output/report.html`, `output/run.log`.

## Modules
- `scope_guard.py`: hostname allowlist, scheme, credentials and port validation.
- `discovery/wayback_miner.py`: historical URL candidates from Wayback CDX.
- `discovery/robots_parser.py`: robots and sitemap hints.
- `discovery/js_extractor.py`: same-scope JS and endpoint candidate extraction.
- `discovery/brute_forcer.py`: tiny, rate-limited local wordlist checks.
- `discovery/google_dorker.py`: generates manual search queries; does not scrape Google.
- `discovery/response_differ.py`: heuristic HTTP response classification.
- `analyzers/content_analyzer.py`: titles, links and form metadata.
- `analyzers/secrets_scanner.py`: redacted pattern matches only.
- `reporters/report_generator.py`: JSON and HTML reports.

## Safety and limitations
No login attempts, form submissions, exploitation, access-control bypass, or redirect following. A URL being found does not mean it is authorized or vulnerable. This is a starter project, not a complete security scanner. Verify authorization, DNS/IP ownership, and network egress controls before production use.
