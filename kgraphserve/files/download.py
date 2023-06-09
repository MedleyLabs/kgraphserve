import functools
import pathlib
import shutil
import requests

from tqdm.auto import tqdm


def download(url, filename):
    """
    Downloads a file from url into filename with progress bar

    :param url: str - Where to download the file from
    :param filename: str - Where to save the file to
    :return path: str - Path to the downloaded file
    """

    r = requests.get(url, stream=True, allow_redirects=True)

    if r.status_code != 200:
        r.raise_for_status()  # Will only raise for 4xx codes, so...
        raise RuntimeError(f'Request to {url} returned status code {r.status_code}')

    file_size = int(r.headers.get('Content-Length', 0))

    path = pathlib.Path(filename).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)

    desc = '(Unknown total file size)' if file_size == 0 else ''
    r.raw.read = functools.partial(r.raw.read, decode_content=True)  # Decompress if needed

    with tqdm.wrapattr(r.raw, 'read', total=file_size, desc=desc) as r_raw:
        with path.open('wb') as f:
            shutil.copyfileobj(r_raw, f)

    return path
