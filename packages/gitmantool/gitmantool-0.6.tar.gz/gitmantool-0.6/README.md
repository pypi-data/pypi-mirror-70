# Git Manager Tool
Console tool for manage projects on github/gitlab

## Installation

Install with pip:

- `pip install gitmantool`

Install from source:

- `git clone https://github.com/katmai1/gitmantool && cd gitmantool`
- `pip install -r requirements.txt`
- `pip install -e`

## Usage

Go to your project folder and execute the new gm command.
First time ask for link of your repo, for example: https://github.com/katmai1/gitmanager


## Development

Requeriments for developers
- `pip install --upgrade setuptools wheel twine`

### How to generate a new version


- Assign version number on file [setup.py](setup.py)
- Commit all changes
- `git tag 0.1 -m "tag description"`
- `git push --tags origin master`

Build package:

- `python setup.py sdist bdist_wheel`

Upload 

- `twine upload -r pypi --skip-existing dist/*`
