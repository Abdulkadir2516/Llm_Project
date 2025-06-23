import requests


def chromium_headers() -> dict:
    return {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Chromium";v="135", "Not-A.Brand";v="8"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    }


def some_cookies() -> dict:
    return {
        'ckns_policy': '000',
        'ckns_privacy': 'july2019',
        'ckns_mvt': 'e7cdb90d-4a2e-4749-b52e-0c7b32144800',
        'ckns_policy_exp': '1765110713575',
        'ckns_sounds_experiments': '{}',
        'ckns_explicit': '1',

    }


def get(url: str) -> str:
    # todo: we need more random headers and cookies for pretending to be a human
    # headers above are for bbc, might need different sets for other sources
    return requests.get(
        url,
        headers=chromium_headers(),
        cookies=some_cookies()).text
