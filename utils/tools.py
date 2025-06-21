from urllib.parse import urlparse, parse_qs, ParseResult


async def get_brand_id(url: str) -> str | None:
    parsed_url: ParseResult = urlparse(url)
    query_params: dict = parse_qs(parsed_url.query)
    return query_params.get('brand_id', [None])[0]

