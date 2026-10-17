import re
PATTERNS = {
 "possible_api_key": re.compile(r'''(?i)(api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]\s*['"]?([A-Za-z0-9_./+=-]{12,})'''),
 "possible_private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
 "possible_cloud_key_id": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
}
def scan_text(text):
    findings = []
    for name, pattern in PATTERNS.items():
        for match in pattern.finditer(text or ""):
            findings.append({"type": name, "location_hint": f"character_offset:{match.start()}", "value": "[REDACTED]"})
    return findings
