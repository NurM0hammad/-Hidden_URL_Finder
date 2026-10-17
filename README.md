# 🔎 Hidden URL Finder

**A Python-based URL Discovery and Analysis Tool for Authorized Security Testing**

Hidden URL Finder helps security researchers and website administrators discover, collect, and analyze URLs within an explicitly authorized website scope. It combines historical URL discovery, JavaScript endpoint extraction, sitemap analysis, HTTP response classification, and report generation.

> ⚠️ **Authorized Use Only:** Use this tool only on websites you own or have explicit permission to assess.

## ✨ Features

- **URL Discovery** — Collect candidate URLs from multiple sources.
- **Wayback URL Mining** — Find historical URLs using the Internet Archive's CDX API.
- **JavaScript Endpoint Extraction** — Identify potential endpoints referenced in JavaScript files.
- **Robots.txt & Sitemap Parsing** — Discover publicly listed paths and sitemap entries.
- **Limited Path Discovery** — Check a small, configurable wordlist with rate limiting.
- **Passive Search Queries** — Generate search engine queries for manual investigation.
- **HTTP Response Analysis** — Classify common HTTP responses and possible soft-404 pages.
- **Content Analysis** — Extract page titles, links, and form metadata.
- **Redacted Secret Pattern Detection** — Flag possible sensitive patterns without including matched values in reports.
- **Scope Guard** — Restrict URL processing to configured hostnames.
- **JSON & HTML Reports** — Save results for review and documentation.
- **Logging** — Record program activity and errors.

## 📁 Project Structure

```text
hidden-url-finder/
├── requirements.txt
├── scope.yaml
├── config.py
├── logger.py
├── scope_guard.py
├── wordlist.txt
├── main.py
├── discovery/
│   ├── __init__.py
│   ├── brute_forcer.py
│   ├── wayback_miner.py
│   ├── js_extractor.py
│   ├── robots_parser.py
│   ├── google_dorker.py
│   └── response_differ.py
├── analyzers/
│   ├── __init__.py
│   ├── content_analyzer.py
│   └── secrets_scanner.py
├── reporters/
│   ├── __init__.py
│   └── report_generator.py
└── output/
    ├── report.json
    ├── report.html
    └── run.log
```

The `output/` directory is generated when the program runs.

## 🛠️ Requirements

- Python 3.10 or newer
- Git
- Internet connection for remote URL discovery
- Authorization to assess the target website

## 💻 Installation

### Windows 11

```powershell
git clone https://github.com/YOUR_USERNAME/hidden-url-finder.git
cd hidden-url-finder

py -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Kali Linux

```bash
git clone https://github.com/YOUR_USERNAME/hidden-url-finder.git
cd hidden-url-finder

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt
```

Replace `YOUR_USERNAME` with your GitHub username.

## ⚙️ Configuration

Edit `scope.yaml` before running the tool.

```yaml
target: "https://example.com"

allowed_hosts:
  - "example.com"
  - "www.example.com"

allow_subdomains: false

request_delay_seconds: 1.0
request_timeout_seconds: 8
max_requests: 60
max_pages: 100
max_js_files: 20
max_wayback_results: 100

user_agent: "HiddenURLFinder/1.0"
```

Replace the example domain with a website you are authorized to assess. List only approved hostnames.

Keep `allow_subdomains: false` unless your authorization explicitly covers subdomains.

## ▶️ Usage

Run the tool from the project root:

```bash
python main.py
```

The tool performs the configured discovery steps and writes reports to the output directory.

## 📊 Reports

| File | Description |
|---|---|
| `output/report.json` | Structured URL discovery results |
| `output/report.html` | HTML report for browser viewing |
| `output/run.log` | Execution logs and warnings |

## 🔐 Security Considerations

- Only assess explicitly authorized websites.
- Configure the hostname allowlist before execution.
- Use conservative request limits and delays.
- Do not commit API keys, passwords, cookies, or other credentials.
- Treat discovered URLs as candidates, not proof of vulnerabilities.
- Treat secret-pattern matches as possible false positives.
- Review scope and network restrictions before any active testing.

**Important:** The scope guard validates hostnames, schemes, credentials, and ports, but it does not independently guarantee DNS/IP-level isolation or protect against every server-side request forgery scenario. Production deployments require additional network controls and security testing.

## ⚠️ Limitations

This is a starter URL inventory and discovery project, not a complete penetration-testing framework.

It does not guarantee discovery of every URL. Search query generation is manual; the tool does not scrape Google. It does not attempt authentication, submit forms, exploit endpoints, or bypass access controls.

## 🗺️ Roadmap

- [ ] Add automated unit tests
- [ ] Improve sitemap index and XML parsing
- [ ] Add CSV export
- [ ] Add configurable crawling depth
- [ ] Improve soft-404 detection
- [ ] Add a local dashboard
- [ ] Add stronger DNS and network-level scope protections

## 🤝 Contributing

Contributions, bug reports, and suggestions are welcome. Please open an issue before submitting major changes.

## 📜 License

Choose an appropriate open-source license before distributing the project. If you intend to use the MIT License, add a `LICENSE` file containing the standard MIT license text and your copyright details.

## 👨‍💻 Author

**YOUR NAME**

GitHub: https://github.com/YOUR_USERNAME

---

**Learn. Build. Secure.**

Use your skills responsibly and respect website owners' authorization and privacy.
