import paramiko
import time

def backup(address: str, user: str, password: str, file: str):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=address, username=user, password=password)

    bkp = f"bkp_{round(time.time())}"
    ssh_client.exec_command(f"system backup save name={bkp}")

    ftp_client = ssh_client.open_sftp()
    ftp_client.get(f"{bkp}.backup", file)
    ftp_client.close()
    
    ssh_client.exec_command(f"file remove {bkp}.backup")
    ssh_client.close()
