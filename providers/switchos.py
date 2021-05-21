import requests
import shutil
from requests.auth import HTTPDigestAuth


def backup(address: str, user: str, password: str, file: str):
    r = requests.get(
        "http://" + address + "/backup.swb",
        auth=HTTPDigestAuth(user, password),
        headers={
            "Referer": "http://" + address,
            "Origin": "http://" + address + "",
        },
        stream=True,
    )

    with open(file, "wb") as out_file:
        shutil.copyfileobj(r.raw, out_file)
