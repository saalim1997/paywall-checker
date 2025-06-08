import urllib.parse


def get_proreader_url(url: str) -> str:
    return f"https://proreader.io/search?url={urllib.parse.quote_plus(url)}"


def make_accessible_url(original_url: str, is_paywalled: bool) -> str:
    if is_paywalled:
        return get_proreader_url(original_url)
    return original_url
