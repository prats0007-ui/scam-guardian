"""Link investigator. It NEVER opens the link; it only checks reputation."""
import difflib

import requests
import tldextract

import config

# Uses the bundled suffix list, so no network call on startup.
_extract = tldextract.TLDExtract(suffix_list_urls=())

# Brands scammers impersonate most. Extend this list over time.
KNOWN_BRANDS = {
    "amazon": "amazon.com", "paypal": "paypal.com", "apple": "apple.com",
    "microsoft": "microsoft.com", "netflix": "netflix.com", "usps": "usps.com",
    "fedex": "fedex.com", "ups": "ups.com", "dhl": "dhl.com",
    "chase": "chase.com", "wellsfargo": "wellsfargo.com",
    "bankofamerica": "bankofamerica.com", "irs": "irs.gov",
    "google": "google.com", "facebook": "facebook.com", "instagram": "instagram.com",
    "whatsapp": "whatsapp.com", "coinbase": "coinbase.com",
}


def lookalike_check(url: str) -> dict:
    ext = _extract(url)
    domain = ext.registered_domain or url
    name = ext.domain.lower().replace("-", "")
    # Undo common character swaps scammers use: amaz0n, paypa1, app1e
    normalized = name.translate(str.maketrans("01358", "olesb"))
    finding = {"url": url, "domain": domain, "lookalike_of": None}
    for brand, official in KNOWN_BRANDS.items():
        if domain == official or name == brand:
            return finding  # real site, or the brand's own country domain
        if len(brand) < 5:  # short names like "ups" or "irs" match too much
            continue
        windows = [normalized[i : i + len(brand)] for i in range(max(1, len(normalized) - len(brand) + 1))]
        similar = any(difflib.SequenceMatcher(None, w, brand).ratio() >= 0.83 for w in windows)
        if brand in normalized or similar:
            finding["lookalike_of"] = official
            break
    return finding


def safe_browsing_check(urls: list[str]) -> set[str]:
    """Returns the set of URLs Google flags as dangerous."""
    if not config.SAFE_BROWSING_API_KEY or not urls:
        return set()
    body = {
        "client": {"clientId": "scam-guardian", "clientVersion": "0.1"},
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE",
                            "POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": u} for u in urls],
        },
    }
    try:
        r = requests.post(
            "https://safebrowsing.googleapis.com/v4/threatMatches:find",
            params={"key": config.SAFE_BROWSING_API_KEY}, json=body, timeout=8,
        )
        r.raise_for_status()
        return {m["threat"]["url"] for m in r.json().get("matches", [])}
    except requests.RequestException:
        return set()


def check_links(urls: list[str]) -> list[dict]:
    flagged = safe_browsing_check(urls)
    results = []
    for url in urls[:5]:
        finding = lookalike_check(url)
        finding["google_flagged"] = url in flagged
        results.append(finding)
    return results
