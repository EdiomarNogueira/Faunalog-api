import requests
from urllib.parse import quote

WIKIPEDIA_BASE = "https://pt.wikipedia.org/api/rest_v1/page/summary"


def get_animal_data(display_name: str):
    try:
        wikipedia_title = display_name.strip()
        encoded_name = quote(wikipedia_title)

        response = requests.get(
            f"{WIKIPEDIA_BASE}/{encoded_name}",
            timeout=8,
            headers={
                "User-Agent": "FaunaDexPortfolioApp/1.0"
            }
        )

        if response.status_code != 200:
            return {
                "image": None,
                "description": "Descrição não encontrada na Wikipédia.",
                "source": None,
            }

        data = response.json()

        image = None

        if data.get("originalimage"):
            image = data["originalimage"].get("source")
        elif data.get("thumbnail"):
            image = data["thumbnail"].get("source")

        return {
            "image": image,
            "description": data.get(
                "extract",
                "Descrição não encontrada na Wikipédia."
            ),
            "source": data.get("content_urls", {})
                .get("desktop", {})
                .get("page"),
        }

    except Exception:
        return {
            "image": None,
            "description": "Erro ao consultar a Wikipédia.",
            "source": None,
        }