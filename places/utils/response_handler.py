from requests.exceptions import HTTPError
from requests.models import Response


def decode_json_response(response: Response):
    response.raise_for_status()
    decoded_response = response.json()
    if 'error' in decoded_response:
        raise HTTPError(decoded_response['error'])
    return decoded_response
