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
