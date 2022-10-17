__version__ = "0.0.6"

import subprocess
from pathlib import Path
from typing import Literal
from datetime import datetime

from cryptography.hazmat.primitives.serialization import pkcs12

from .exceptions import (
    InvalidCertificatePath,
    InvalidCertificatePassword,
    InvalidStoreLocation,
)


class Certificate:

    STORE_LOCATIONS = {
        "user": "Cert:\CurrentUser\My",
        "machine": "Cert:\LocalMachine\My",
    }

    def __init__(self, certificate_path: str | Path, password: str) -> None:
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
        if type(self._path) not in [str, Path]:
            raise InvalidCertificatePath()
        if self._path is not None:
            with open(self._path, "rb") as certificate_data:
                _, self._object, _ = pkcs12.load_key_and_certificates(
                    certificate_data.read(),
                    bytes(self._password, "utf-8"),
                )

    def install(
        self,
        store_location: Literal["user", "machine"] = "user",
        exportable: bool = False,
        verbose: bool = False,
    ) -> None:
        """Install certificate"""
        try:
            store_location_value = self.STORE_LOCATIONS[store_location]
        except KeyError as exc:
            raise InvalidStoreLocation() from exc
        command = f"powershell.exe $password=ConvertTo-SecureString -String '{self._password}' -AsPlainText -Force;"
        command += f" Import-PfxCertificate -FilePath {self._path} -Password $password"
        command += f" -CertStoreLocation {store_location_value} {'-Exportable' if exportable else ''}"
        subprocess.run(command, capture_output=not verbose)

    @classmethod
    def remove(
        cls,
        cn: str,
        store_location: Literal["user", "machine"] = "user",
        verbose: bool = False,
    ) -> None:
        """Search certificate by CN (Common Name) and remove it"""
        try:
            store_location_value = cls.STORE_LOCATIONS[store_location]
        except KeyError as exc:
            raise InvalidStoreLocation() from exc
        command = f"powershell.exe Get-ChildItem {store_location_value} |"
        command += f" Where-Object Subject -match 'CN={cn}' | Remove-Item"
        subprocess.run(command, capture_output=not verbose)

    def get_subject_data(self) -> list[str]:
        """Returns a list with certificate's subject data"""
        return [c.rfc4514_string() for c in self._object.subject.rdns]

    def get_expiration_date(self) -> datetime | None:
        """Returns datetime object with certificate's experation date"""
        return self._object.not_valid_after

    def get_issue_date(self) -> datetime | None:
        """Returns datetime object with the date the certificate was issued"""
        return self._object.not_valid_before
