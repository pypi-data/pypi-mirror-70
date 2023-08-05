![JSON-Secrets](https://raw.githubusercontent.com/marcoEDU/JSON-Secrets/master/images/headerimage.jpg "JSON-Secrets")

Load your secrets (API keys etc.) from a JSON file.

Want to support the development and stay updated?

<a href="https://www.patreon.com/bePatron?u=24983231"><img alt="Become a Patreon" src="https://raw.githubusercontent.com/marcoEDU/JSON-Secrets/master/images/patreon_button.svg"></a> <a href="https://liberapay.com/glowingkitty/donate"><img alt="Donate using Liberapay" src="https://liberapay.com/assets/widgets/donate.svg"></a>

## Installation
```
pip install jsonsecrets
```

## Usage
```
from jsonsecrets import Secret

password = Secret(target='example_api.user.password',file_path='mysecrets.json').value
```