import paramiko


def backup(address: str, user: str, password: str, file: str):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=address, username=user, password=password)

    ftp_client = ssh_client.open_sftp()
    ftp_client.get("/conf/config.xml", file)
    ftp_client.close()
