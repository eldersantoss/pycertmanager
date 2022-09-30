__version__ = "0.0.2"

import subprocess
from pathlib import Path
from datetime import datetime

from cryptography.hazmat.primitives.serialization import pkcs12

from pycertmanager.exceptions import InvalidCertificatePath, InvalidCertificatePassword


class Certificate:
    def __init__(
        self,
        certificate_path: str | Path | None = None,
        password: str | None = None,
    ) -> None:
        self._path = certificate_path
        self._password = password
        self._object = None
        try:
            self._validate_kwargs_and_read_certificate()
        except FileNotFoundError as exc:
            raise InvalidCertificatePath() from exc
        except (ValueError, TypeError) as exc:
            raise InvalidCertificatePassword() from exc

    def _validate_kwargs_and_read_certificate(self) -> None:
        if type(self._path) not in [str, Path, type(None)]:
            raise InvalidCertificatePath()
        if self._path is not None:
            with open(self._path, "rb") as certificate_data:
                _, self._object, _ = pkcs12.load_key_and_certificates(
                    certificate_data.read(),
                    bytes(self._password, "utf-8"),
                )

    def install(
        self,
        store_location="Cert:\CurrentUser\My",
        exportable=False,
        verbose=False,
    ):
        """Install certificate"""
        command = f"powershell.exe $password=ConvertTo-SecureString -String '{self._password}' -AsPlainText -Force;"
        command += f" Import-PfxCertificate -FilePath {self._path} -Password $password"
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

    def get_subject_data(self) -> list[str]:
        """Returns a list with subject data of certificate"""
        if self._object is not None:
            return [c.rfc4514_string() for c in self._object.subject.rdns]
        return []

    def get_expiration_date(self) -> datetime:
        if self._object is not None:
            return self._object.not_valid_after
        return None

    def get_expedition_date(self) -> datetime:
        if self._object is not None:
            return self._object.not_valid_before
        return None
