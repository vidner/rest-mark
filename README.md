# rest-mark
benchmark rest api with python requests

## Install Dependencies
```bash
$ pip install -r requirements.txt
```
## Usage
```bash
$ python3 rest-mark.py --help
Usage: rest-mark.py [OPTIONS] METHOD

  available methods : get,post,put,delete

Options:
  -n, --count INTEGER   number of request
  -u, --url TEXT        api url  [required]
  -s, --single          single thread, by default is multi-thread
  -w, --worker INTEGER  default worker is 10
  -d, --data TEXT       in json format
  -h, --headers TEXT    in json format
  --help                Show this message and exit.

```
## Example
![Alt text](./term.svg)
