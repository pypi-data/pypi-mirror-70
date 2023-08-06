# requests-adapter-injector

This package provides a global mechanism for injection of [Requests](https://requests.readthedocs.io/en/master/)
transport adapters. Injection is done with the help of [importhook](https://pypi.org/project/importhook/)
library and a `.pth` file as described
[here](https://stackoverflow.com/questions/40484942/how-to-execute-python-code-on-interpreter-startup-in-virtualenv/57718902#57718902).
You may probably want to use this package in a separate venv, where you would install
Python tools using Requests which you want to inject transport adapters into, along with
a package implementing desired adapters to inject. You may want to try [pipx](https://pypi.org/project/pipx/) tool
to manage venvs for Python-based tools.
With that you would probably do `pipx install <target-tool> && pipx inject <target-tool> <adapter-package>`.

This package itself can be tested using the built-in test transport adapter, which can also serve as an example
for authors of adapter packages.

```
$ python -mvenv venv
$ venv/bin/pip install requests-adapter-injector
$ venv/bin/python -c "import requests; r = requests.get('injector-test://some/url'); print(r.json())"
{'method': 'GET', 'url': 'injector-test://some/url', 'headers': {'User-Agent': 'python-requests/2.23.0', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}, 'body': None}
```

Adapter packages have to declare one or more `requests_adapter_injector.adapter` entry_points, and are expected
to require this package, to have it installed automatically.

Note: this package will not work when installed as editable install because
`src/requests_adapter_injector.pth` is not installed then.

## Existing transport adapter packages

None so far and some in planning.
