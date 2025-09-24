import requests


def get_token(tenant_id: int, referer: str) -> dict:
    """
    Получает актуальный Bearer токен для Profitbase site_widget.

    Args:
        tenant_id: ID арендатора (например, 4242)
        referer: URL сайта, с которого вызывается виджет (пример: 'https://xn--80abdl0adtby.xn--p1ai')

    Returns:
        dict с заголовком Authorization для requests:
            {"authorization": "Bearer <token>"}
    """
    url = "https://sso.profitbase.ru/api/oauth2/token"

    payload = {
        "client_id": "site_widget",
        "client_secret": "site_widget",
        "grant_type": "site_widget",
        "scope": "SITE_WIDGET",
        "referer": referer
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-tenant-id": str(tenant_id),
        "origin": referer,
        "referer": referer,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    }

    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()

    token = resp.json().get("access_token")
    if not token:
        raise ValueError("Не удалось получить токен из ответа: {}".format(resp.text))

    return {"authorization": f"Bearer {token}"}