__version__ = "0.0.2"

import subprocess
from pathlib import Path


class Certificate:
    def __init__(self, certificate_path: str | Path, password: str) -> None:
        self._certificate_path = certificate_path
        self._password = password

    def install(
        self,
        store_location="Cert:\CurrentUser\My",
        exportable=False,
        verbose=False,
    ):
        """Install certificate"""
        command = f"powershell.exe $password=ConvertTo-SecureString -String '{self._password}' -AsPlainText -Force;"
        command += f" Import-PfxCertificate -FilePath {self._certificate_path} -Password $password"
        command += f" -CertStoreLocation {store_location} {'-Exportable' if exportable else ''}"
        subprocess.run(command, capture_output=not verbose)
