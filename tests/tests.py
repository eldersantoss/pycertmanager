import unittest
import subprocess
from datetime import datetime

from pycertmanager import Certificate


class TestCertificate(unittest.TestCase):
    def test_install(self):
        """Test if certificate has been installed correctly"""

        # ensuring that test certificate is not installed
        self._remove_test_certificate()

        # getting number of certificates before installing
        old_num_of_certificates = self._get_number_of_installed_certificates()

        # instantiating Certificate object and installing it
        certificate = Certificate(
            "assets/pycertmanager_test_password_123456.pfx",
            "123456",
        )
        certificate.install()

        # getting number of certificates after installing
        new_num_of_certificates = self._get_number_of_installed_certificates()

        # comparing them
        self.assertGreater(
            new_num_of_certificates,
            old_num_of_certificates,
            "Number of installed certificates must have been incremented",
        )

        # removing test certificate
        self._remove_test_certificate()

    def test_remove(self):
        """Test if certificate has been removed correctly"""

        # ensuring that test certificate is installed
        self._install_test_certificate()

        # getting number of certificates before removing
        old_num_of_certificates = self._get_number_of_installed_certificates()

        # instantiating Certificate object and removing test certificate
        certificate = Certificate()
        certificate.remove(cn="pycertmanager.test")

        # getting number of certificates after removing
        new_num_of_certificates = self._get_number_of_installed_certificates()

        # comparing them
        self.assertGreater(
            old_num_of_certificates,
            new_num_of_certificates,
            "Number of installed certificates must have been decremented",
        )

    def test_get_subject_data(self):
        """Test if subject data is returned correctly"""

        # ensuring that test certificate is installed
        self._install_test_certificate()

        # instantiating bound Certificate object
        certificate = Certificate(
            "assets/pycertmanager_test_password_123456.pfx",
            "123456",
        )

        # getting list with subject data
        subject_data = certificate.get_subject_data()

        # checking if it's correct
        self.assertListEqual(
            subject_data,
            ["CN=pycertmanager.test"],
            "Subject data must have CN information from test certificate",
        )

        # instantiating unbound Certificate object
        certificate = Certificate()

        # getting list with subject data
        subject_data = certificate.get_subject_data()

        # checking if it's correct
        self.assertListEqual(
            subject_data,
            [],
            "Subject data must be empty",
        )

        # removing test certificate
        self._remove_test_certificate()

    def test_get_expiration_date(self):
        """Test if expiration date is returned correctly"""

        # ensuring that test certificate is installed
        self._install_test_certificate()

        # instantiating bound Certificate object
        certificate = Certificate(
            "assets/pycertmanager_test_password_123456.pfx",
            "123456",
        )
        correct_date = datetime(2023, 9, 28, 4, 6, 8)

        # getting expiration date
        expiration_date = certificate.get_expiration_date()

        # checking if it's correct
        self.assertEqual(
            expiration_date,
            correct_date,
            f"Expiration date must have been {correct_date}",
        )

        # removing test certificate
        self._remove_test_certificate()

    def _get_number_of_installed_certificates(self) -> int:
        """Help function to get number of installed certificates"""
        command = "powershell.exe Get-ChildItem Cert:\CurrentUser\My"
        result = subprocess.run(command, capture_output=True)
        try:
            num_of_certificates = result.stdout.decode("utf-8").strip().splitlines()[4:]
        except IndexError:
            num_of_certificates = 0
        return len(num_of_certificates)

    def _install_test_certificate(self) -> None:
        """Help function to install test certificate"""
        command = f"powershell.exe $password=ConvertTo-SecureString -String '123456' -AsPlainText -Force;"
        command += f" Import-PfxCertificate -FilePath 'assets/pycertmanager_test_password_123456.pfx' -Password $password"
        command += f" -CertStoreLocation Cert:\CurrentUser\My"
        subprocess.run(command, capture_output=True)

    def _remove_test_certificate(self) -> None:
        """Help function to remove test certificate"""
        subprocess.run(
            "powershell.exe Get-ChildItem Cert:\CurrentUser\My | Where-Object Subject -match 'pycertmanager.test' | Remove-Item",
            capture_output=True,
        )
