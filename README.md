# Python Certificate Manager

Module to assist in the programmatic management of `PFX` digital certificates on
`Windows` operating system.

Working with A1 digital certificates (e-CPF and e-CNPJ), it is extremely common
to need to install and remove them from operating system, or even obtain some
information like expiration date or issuer of these objects. So this module
was made for provide these operations programmatically and easily.

[![License](https://img.shields.io/github/license/eldersantoss/pycertmanager)](https://github.com/eldersantoss/pycertmanager/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/eldersantoss/pycertmanager)](https://github.com/eldersantoss/pycertmanager/issues)
[![Version](https://img.shields.io/pypi/v/pycertmanager)](https://pypi.org/project/pycertmanager/)
[![Last commit](https://img.shields.io/github/last-commit/eldersantoss/pycertmanager)](https://github.com/eldersantoss/pycertmanager/commits/main)
[![Tesing](https://github.com/eldersantoss/pycertmanager/actions/workflows/tesing.yml/badge.svg)](https://github.com/eldersantoss/pycertmanager/actions/workflows/tesing.yml)
![Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/eldersantoss/c26a50f51f846509ef4ca4ab5c37909b/raw/coverage.json)

## Table of content

* [Installing](#installing)
    * [Requirements](#requirements)
* [Using](#using)
    * [Examples](#examples)
* [How does it works](#how-does-it-works)
* [Support](#support)
* [Contributing](#contributing)
    * [Setup your environment (Windows PowerShell)](#setup-your-environment-windows-powershell)
* [Roadmap](#roadmap)
* [License](#license)


## Installing

```powershell
pip install pycertmanager
```

### Requirements

The module currently supports only `Windows` operating system and has been tested over `Python >= 3.10`.


## Using

The main entity of the module is the `Certificate` class which provides the
methods for manipulating certificates within the operating system and
obtaining relevant information from them.

### Examples

```python
from pycertmanager import Certificate

# creating certificate object
certificate = Certificate("mycertificate.pfx", "123456")

# installing certificate on system
certificate.install()

# getting a list with certificate subject data
subject_data = certificate.get_subject_data()

# getting certificate expiration date
expiration_date = certificate.get_expiration_date()

# getting certificate expiration date
issue_date = certificate.get_issue_date()

# removing a certificate
# note that it is a class method and 'pycertmanager.test' is the
# Common Name (CN) of the certificate you want to remove
Certificate.remove("pycertmanager.test")
```

## How does it works

In short, some methods (install and remove) calls
[PowerShell cmdlets](https://learn.microsoft.com/en-us/powershell/module/pki/)
through subprocess built-in module while the remaining methods uses
[cryptography](https://github.com/pyca/cryptography) package primitives.

## Support

Found a problema? Please open an `Issue` describing it or a `Pull Request` if
you know how to fix it. Make sure to write the `tests` from your code.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to
discuss what you would like to change. Reinforcing, make sure to write tests from your code.

### Setup your environment (Windows PowerShell)

```powershell
# clone this repository
git clone https://github.com/eldersantoss/pycertmanager.git

# create and activate virtual environment
cd pycertmanager
python -m venv venv
& venv/Scripts/Activate

# install dependencies
pip install -r requirements.txt

# run tests
python -m unittest
```

## Roadmap

* **Implement Linux support:** the intention is to make this module
cross-platform. 

## License

This project is licensed under the terms of the [MIT License](https://github.com/eldersantoss/pycertmanager/blob/main/LICENSE).
