import unittest
import subprocess

from pycertmanager import Certificate


class TestCertificate(unittest.TestCase):
    def test_install(self):
        """Test if certificate has been installed correctly"""

        # getting number of certificates before installing
        command = "powershell.exe Get-ChildItem Cert:\CurrentUser\My"
        result = subprocess.run(command, capture_output=True)
        old_num_of_certificates = len(
            result.stdout.decode("utf-8").strip().splitlines()
        )

        # instantiating Certificate object and installing it
        certificate = Certificate(
            "assets/pycertmanager_test_password_123456.pfx",
            "123456",
        )
        certificate.install()

        # getting number of certificates after installing
        result = subprocess.run(command, capture_output=True)
        new_num_of_certificates = len(
            result.stdout.decode("utf-8").strip().splitlines()
        )

        # comparing them
        self.assertGreater(
            new_num_of_certificates,
            old_num_of_certificates,
            "Number of installed certificates must have been incremented",
        )

        # removing installed certificate
        subprocess.run(
            "powershell.exe Get-ChildItem Cert:\CurrentUser\My | Where-Object {$_.Subject -match 'pycertmanager.test'} | Remove-Item",
            capture_output=True,
        )

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
        """Help function to install test certificate"""
        subprocess.run(
            "powershell.exe Get-ChildItem Cert:\CurrentUser\My | Where-Object Subject -match 'pycertmanager.test' | Remove-Item",
            capture_output=True,
        )
