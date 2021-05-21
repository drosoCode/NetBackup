import requests
import shutil


def backup(address: str, user: str, password: str, file: str):
    h = {
        "Referer": "http://" + address,
        "Origin": "http://" + address + "",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    login = requests.post(
        "http://" + address + "/cgi-bin/luci",
        headers=h,
        data={"luci_username": user, "luci_password": password},
        allow_redirects=False,
    )
    token = requests.utils.dict_from_cookiejar(login.cookies)["sysauth"]

    r = requests.post(
        "http://" + address + "/cgi-bin/cgi-backup",
        headers=h,
        data={"sessionid": token},
        stream=True,
    )

    with open(file, "wb") as out_file:
        shutil.copyfileobj(r.raw, out_file)
