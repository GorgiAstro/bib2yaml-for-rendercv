# bib2yaml-for-rendercv

## Installation

Install the dependencies with `pip install .`, which will install the library as well as the CLI entrypoint named `bib2yaml`.

## CLI usage

Run the CLI with `bib2yaml`. CLI options are:

* `-i` or `--input-file`: input file path. Defaut is `pubs.bib`
* `-o` or `--output-file`: output file path. Defaut is `pubs.yml`
* `-n` or `--n-max-authors`: max numbers of authors to display. When higher than this treshold, only the first author is shown, the rest is displayed as "et al".

## Usage as library

```python
from bib2yaml.bib2yaml import convert_bib
convert_bib("<INPUT PATH>", "<OUTPUT PATH>", n_max_authors)
```
