import unittest
import subprocess
from datetime import datetime

from pycertmanager import Certificate
from pycertmanager.exceptions import (
    InvalidCertificatePath,
    InvalidCertificatePassword,
    InvalidStoreLocation,
)


class TestCertificate(unittest.TestCase):

    TEST_CERT_PATH = "tests/assets/pycertmanager_test_password_123456.pfx"
    TEST_CERT_PASSWORD = "123456"
    TEST_CERT_CN = "pycertmanager.test"
    TEST_CERT_STORE_LOCATION = "Cert:\CurrentUser\My"

    def test_constructor(self):
        """Tests if certificate is created correctly"""

        certificate = Certificate(self.TEST_CERT_PATH, self.TEST_CERT_PASSWORD)
        self.assertEqual(
            certificate._path,
            self.TEST_CERT_PATH,
            "_path attribute must be equal to test certificate path",
        )
        self.assertEqual(
            certificate._password,
            self.TEST_CERT_PASSWORD,
            "_password attribute must be equal to test certificate password",
        )
        self.assertIsNotNone(
            certificate._object,
            "_object attribute must not be None",
        )

    def test_constructor_with_invalid_path(self):
        """Tests if constructor raises InvalidCertificatePath exception"""

        with self.assertRaises(InvalidCertificatePath):
            Certificate(None, self.TEST_CERT_PASSWORD)
        with self.assertRaises(InvalidCertificatePath):
            Certificate("", self.TEST_CERT_PASSWORD)
        with self.assertRaises(InvalidCertificatePath):
            Certificate(0, self.TEST_CERT_PASSWORD)
        with self.assertRaises(InvalidCertificatePath):
            Certificate(True, self.TEST_CERT_PASSWORD)

    def test_constructor_with_invalid_password(self):
        """Tests if constructor raises InvalidCertificatePassword exception"""

        with self.assertRaises(InvalidCertificatePassword):
            Certificate(self.TEST_CERT_PATH, None)
        with self.assertRaises(InvalidCertificatePassword):
            Certificate(self.TEST_CERT_PATH, "123")
        with self.assertRaises(InvalidCertificatePassword):
            Certificate(self.TEST_CERT_PATH, 123)
        with self.assertRaises(InvalidCertificatePassword):
            Certificate(self.TEST_CERT_PATH, True)

    def test_install(self):
        """Test if certificate has been installed correctly"""

        # ensuring that test certificate is not installed
        self._remove_test_certificate()

        # getting number of certificates before installing
        old_num_of_certificates = self._get_number_of_installed_certificates()

        # instantiating Certificate object and installing it
        certificate = Certificate(self.TEST_CERT_PATH, self.TEST_CERT_PASSWORD)
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

    def test_install_with_invalid_store_location(self):
        """Tests if InvalidStoreLocation exception is raised"""

        certificate = Certificate(self.TEST_CERT_PATH, self.TEST_CERT_PASSWORD)
        with self.assertRaises(InvalidStoreLocation):
            certificate.install(store_location="")

    def test_remove(self):
        """Test if certificate has been removed correctly"""

        # ensuring that test certificate is installed
        self._install_test_certificate()

        # getting number of certificates before removing
        old_num_of_certificates = self._get_number_of_installed_certificates()

        # removing test certificate
        Certificate.remove("pycertmanager.test")

        # getting number of certificates after removing
        new_num_of_certificates = self._get_number_of_installed_certificates()

        # comparing them
        self.assertGreater(
            old_num_of_certificates,
            new_num_of_certificates,
            "Number of installed certificates must have been decremented",
        )

    def test_remove_with_invalid_store_location(self):
        """Tests if InvalidStoreLocation exception is raised"""

        with self.assertRaises(InvalidStoreLocation):
            Certificate.remove("", store_location="")

    def test_get_subject_data(self):
        """Test if subject data is returned correctly"""

        # ensuring that test certificate is installed
        self._install_test_certificate()

        # instantiating Certificate object
        certificate = Certificate(self.TEST_CERT_PATH, self.TEST_CERT_PASSWORD)

        # getting a list with subject data
        subject_data = certificate.get_subject_data()

        # checking if it's correct
        self.assertListEqual(
            subject_data,
            ["CN=pycertmanager.test"],
            "Subject data must have CN information from test certificate",
        )

        # removing test certificate
        self._remove_test_certificate()

    def test_get_expiration_date(self):
        """Test if expiration date is returned correctly"""

        # ensuring that test certificate is installed
        self._install_test_certificate()

        # instantiating Certificate object
        certificate = Certificate(
            self.TEST_CERT_PATH,
            self.TEST_CERT_PASSWORD,
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

    def test_get_issue_date(self):
        """Test if issue date is returned correctly"""

        # ensuring that test certificate is installed
        self._install_test_certificate()

        # instantiating Certificate object
        certificate = Certificate(self.TEST_CERT_PATH, self.TEST_CERT_PASSWORD)
        correct_date = datetime(2022, 9, 28, 3, 46, 8)

        # getting issue date
        issue_date = certificate.get_issue_date()

        # checking if it's correct
        self.assertEqual(
            issue_date,
            correct_date,
            f"Issue date must have been {correct_date}",
        )

        # removing test certificate
        self._remove_test_certificate()

    def _get_number_of_installed_certificates(self) -> int:
        """Help function to get number of installed certificates"""
        command = f"powershell.exe Get-ChildItem {self.TEST_CERT_STORE_LOCATION}"
        result = subprocess.run(command, capture_output=True)
        try:
            num_of_certificates = result.stdout.decode("utf-8").strip().splitlines()[4:]
        except IndexError:
            num_of_certificates = 0
        return len(num_of_certificates)

    def _install_test_certificate(self) -> None:
        """Help function to install test certificate"""
        command = f"powershell.exe $password=ConvertTo-SecureString -String '{self.TEST_CERT_PASSWORD}' -AsPlainText -Force;"
        command += f" Import-PfxCertificate -FilePath '{self.TEST_CERT_PATH}' -Password $password"
        command += f" -CertStoreLocation {self.TEST_CERT_STORE_LOCATION}"
        subprocess.run(command, capture_output=True)

    def _remove_test_certificate(self) -> None:
        """Help function to remove test certificate"""
        command = f"powershell.exe Get-ChildItem {self.TEST_CERT_STORE_LOCATION} |"
        command += f"Where-Object Subject -match '{self.TEST_CERT_CN}' | Remove-Item"
        subprocess.run(command, capture_output=True)
