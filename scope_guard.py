from urllib.parse import urlsplit, urlunsplit
import ipaddress
class ScopeError(ValueError): pass
class ScopeGuard:
    def __init__(self, config):
        self.allowed_hosts = {str(h).strip().lower().rstrip(".") for h in config["allowed_hosts"]}
        self.allow_subdomains = bool(config.get("allow_subdomains", False))
        if not self.allowed_hosts: raise ScopeError("allowed_hosts is empty")
    def check(self, url, require_http=True):
        if not isinstance(url, str) or len(url) > 4096: raise ScopeError("Invalid URL")
        p = urlsplit(url.strip())
        if require_http and p.scheme.lower() not in ("http", "https"): raise ScopeError("Only HTTP/HTTPS URLs are allowed")
        if not p.hostname: raise ScopeError("URL has no hostname")
        if p.username or p.password: raise ScopeError("Credentials in URLs are not allowed")
        host = p.hostname.lower().rstrip(".")
        try: ipaddress.ip_address(host); is_ip = True
        except ValueError: is_ip = False
        permitted = host in self.allowed_hosts
        if self.allow_subdomains:
            permitted = permitted or any(host.endswith("." + h) for h in self.allowed_hosts)
        if not permitted: raise ScopeError(f"Host outside authorized scope: {host}")
        if is_ip and host not in self.allowed_hosts: raise ScopeError("IP literal not explicitly listed")
        if p.port and p.port not in (80, 443): raise ScopeError("Non-standard ports disabled")
        return urlunsplit((p.scheme.lower(), p.netloc, p.path or "/", p.query, ""))
    def same_scope(self, url):
        try: self.check(url); return True
        except (ScopeError, ValueError): return False
