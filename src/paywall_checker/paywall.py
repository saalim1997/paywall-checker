import cloudscraper


def is_accessible(url):
    try:
        scraper = cloudscraper.create_scraper()
        resp = scraper.get(url)
        html = resp.text.lower()
        print(html)
        # Simple keyword check for paywall
        for keyword in [
            "subscribe",
            "paywall",
            "register",
            "gain access",
            "see subscription options",
        ]:
            if keyword in html:
                return False
        return True
    except Exception:
        return False
        return False
