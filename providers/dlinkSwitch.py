import requests
import hashlib
import shutil


def backup(address: str, user: str, password: str, file):
    password = hashlib.md5(password.encode("utf-8")).hexdigest()

    login = requests.post(
        "http://" + address + "/cgi/login.cgi",
        cookies={"Gambit": "login"},
        data={"pass": password},
    ).text

    cookies = {
        "Gambit": login[login.find("Gambit=") + 7 : login.rfind(";path=/")],
        "SessID": login[login.find("SessID=") + 7 : login.find(";path=/")],
    }
    requests.post(
        "http://" + address,
        cookies=cookies,
        headers={
            "Referer": "http://" + address + "/cgi/login.cgi",
        },
    )

    r = requests.post(
        "http://" + address + "/cgi/FWBackup.cgi",
        cookies=cookies,
        headers={
            "Referer": "http://"
            + address
            + "/DGS-1100-08_1.00.016/iss/H_03_Firmware.htm",
            "Origin": "http://" + address + "",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
        },
        stream=True,
    )

    with open(file, "wb") as out_file:
        shutil.copyfileobj(r.raw, out_file)
