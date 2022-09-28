__version__ = "0.0.2"

import subprocess
from pathlib import Path


class Certificate:
    def __init__(
        self,
        certificate_path: str | Path | None = None,
        password: str | None = None,
    ) -> None:
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

    def remove(
        self,
        cn,
        store_location="Cert:\CurrentUser\My",
        verbose=False,
    ):
        """Search certificate by CN (Common Name) and remove it"""
        command = f"powershell.exe Get-ChildItem {store_location} |"
        command += f" Where-Object Subject -match 'CN={cn}' | Remove-Item"
        subprocess.run(command, capture_output=not verbose)
