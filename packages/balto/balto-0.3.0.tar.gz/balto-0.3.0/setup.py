# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['balto',
 'balto.displayer',
 'balto.interfaces',
 'balto.interfaces.curses',
 'balto.runners']

package_data = \
{'': ['*'],
 'balto': ['web_interfaces/balto_react/*',
           'web_interfaces/balto_react/.cache/*',
           'web_interfaces/balto_react/.storybook/*',
           'web_interfaces/balto_react/build/*',
           'web_interfaces/balto_react/build/static/css/*',
           'web_interfaces/balto_react/build/static/js/*',
           'web_interfaces/balto_react/node_modules/*',
           'web_interfaces/balto_react/node_modules/.bin/*',
           'web_interfaces/balto_react/node_modules/.cache/babel-loader/*',
           'web_interfaces/balto_react/node_modules/.cache/eslint-loader/*',
           'web_interfaces/balto_react/node_modules/.cache/terser-webpack-plugin/content-v2/sha512/85/80/*',
           'web_interfaces/balto_react/node_modules/.cache/terser-webpack-plugin/content-v2/sha512/ce/b3/*',
           'web_interfaces/balto_react/node_modules/.cache/terser-webpack-plugin/content-v2/sha512/e5/f6/*',
           'web_interfaces/balto_react/node_modules/.cache/terser-webpack-plugin/index-v5/b9/ce/*',
           'web_interfaces/balto_react/node_modules/.cache/terser-webpack-plugin/index-v5/bb/fa/*',
           'web_interfaces/balto_react/node_modules/.cache/terser-webpack-plugin/index-v5/f2/b5/*',
           'web_interfaces/balto_react/public/*',
           'web_interfaces/balto_react/src/*',
           'web_interfaces/balto_react/src/components/*',
           'web_interfaces/balto_react/src/containers/*',
           'web_interfaces/balto_react/src/images/*',
           'web_interfaces/balto_react/src/stories/*',
           'web_interfaces/simple/*',
           'web_interfaces/simple/src/*',
           'web_interfaces/simple/src/styles/*',
           'web_interfaces/simple/static/css/*',
           'web_interfaces/simple/static/js/*']}

install_requires = \
['aiodocker>=0.14.0,<0.15.0',
 'aiofiles>=0.4.0,<0.5.0',
 'click>=7.0,<8.0',
 'docker>=3.5,<4.0',
 'email-validator>=1.0,<2.0',
 'fastapi>=0.35.0,<0.36.0',
 'npyscreen>=4.10,<5.0',
 'prompt_toolkit>=2.0,<3.0',
 'tomlkit>=0.5.5,<0.6.0',
 'urwid>=2.0,<3.0',
 'uvicorn>=0.8.6,<0.9.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.6.0,<0.7.0']}

entry_points = \
{'console_scripts': ['balto = balto.cli:main',
                     'balto-curses = balto.interfaces.curses:main',
                     'balto-server = balto.new_server:main']}

setup_kwargs = {
    'name': 'balto',
    'version': '0.3.0',
    'description': 'BAlto is a Language independent Test Orchestrator',
    'long_description': '# ![Logo of Balto](logo-100x.png) BALTO\n[![All Contributors](https://img.shields.io/badge/all_contributors-3-orange.svg?style=flat-square)](#contributors-)\n\n`BAlto is a Language independent Test Orchestrator` is an unique tool to drive\nall your test-runners with one common interface.\n\n## Installation\n\nInstall balto with [pipx](https://github.com/cs01/pipx):\n\n```bash\npipx install balto\n```\n\nYou should see at the end of the command:\n\n```\n  These binaries are now globally available\n    - balto\n    - balto-curses\n    - balto-server\ndone! ✨ 🌟 ✨\n\n```\n\nIt is highly recommended to avoid installing Balto in either your global Python environment or a virtual environment as it might causes conflicts with some dependencies.\n\n## Usage\n\nTo use it, point balto to a directory containing a `.balto.toml` file:\n    \n```bash\nbalto tests/\n```\n\nThe `.balto.toml` file should look like:\n\n```toml\nname = "Acceptance Test Suite Subprocess"\ntool = "pytest"\n\n```\n\nIf you just want to give Balto a try, you can use the `--tool` to indicate which tool you want to use. For example:\n\n```\nbalto --tool pytest tests\n```\n\nThe tool must be one of the supported one, you can see the list here: https://github.com/lothiraldan/litf#compatible-emitters\n\nYou can test balto against examples for supported test runners. Clone this repository and launch `balto` against one of the examples directories. For `pytest`, launch:\n\n```bash\nbalto examples/pytest/\n```\n\nFor more help:\n\n```bash\nbalto --help\n```\n\n\n## Development\n\nBalto is composed of two components: the server and the web interface.\n\n> Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms. Please report unacceptable behavior to [lothiraldan@gmail.com](lothiraldan@gmail.com).\n\n### Balto-server\n\nBalto-server is a Python 3.7 project using Asyncio. To build the development version, first create a virtualenv (or equivalent):\n\n```bash\nvirtualenv .venv\nsource .venv/bin/activate\n```\n\nInstall the project in development mode:\n\n```bash\npip install -e .\n```\n\nThen start the server:\n\n```bash\nbalto-server --debug examples/pytest/\n```\n\nThe server will start on port 8889.\n\n### Web interface\n\nThe web interface is a React project communicating with the server using WebSockets. You can start developing on it with these instructions:\n\n```bash\ncd balto/web_interfaces/balto_react\nyarn start\n```\n\nThe web interface is then available on http://localhost:3000/ and will connect to the server started before.\n\nWarning: the WebSocket doesn\'t auto-reconnect yet, sometimes your React modification requires you to reload your browser tab.\n\n## Contributors\n\nThanks goes to these wonderful people ([emoji key](https://github.com/kentcdodds/all-contributors#emoji-key)):\n\n<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->\n<!-- prettier-ignore-start -->\n<!-- markdownlint-disable -->\n<table>\n  <tr>\n    <td align="center"><a href="https://lothiraldan.github.io/"><img src="https://avatars2.githubusercontent.com/u/243665?v=4" width="100px;" alt=" Boris Feld"/><br /><sub><b> Boris Feld</b></sub></a><br /><a href="https://github.com/lothiraldan/balto/commits?author=Lothiraldan" title="Code">💻</a> <a href="#design-Lothiraldan" title="Design">🎨</a> <a href="https://github.com/lothiraldan/balto/commits?author=Lothiraldan" title="Documentation">📖</a> <a href="#ideas-Lothiraldan" title="Ideas, Planning, & Feedback">🤔</a> <a href="#talk-Lothiraldan" title="Talks">📢</a></td>\n    <td align="center"><a href="https://eliasdorneles.github.io"><img src="https://avatars0.githubusercontent.com/u/37565?v=4" width="100px;" alt="Elias Dorneles"/><br /><sub><b>Elias Dorneles</b></sub></a><br /><a href="https://github.com/lothiraldan/balto/commits?author=eliasdorneles" title="Code">💻</a> <a href="https://github.com/lothiraldan/balto/issues?q=author%3Aeliasdorneles" title="Bug reports">🐛</a></td>\n    <td align="center"><a href="https://github.com/madprog"><img src="https://avatars0.githubusercontent.com/u/539272?v=4" width="100px;" alt="Paul Morelle"/><br /><sub><b>Paul Morelle</b></sub></a><br /><a href="https://github.com/lothiraldan/balto/commits?author=madprog" title="Code">💻</a></td>\n  </tr>\n</table>\n\n<!-- markdownlint-enable -->\n<!-- prettier-ignore-end -->\n<!-- ALL-CONTRIBUTORS-LIST:END -->\n\nThis project follows the [all-contributors](https://github.com/kentcdodds/all-contributors) specification. Contributions of any kind welcome!',
    'author': 'Boris Feld',
    'author_email': 'lothiraldan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://lothiraldan.github.io/balto/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
