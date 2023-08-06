# mdict.py
Python API for mdict IO (MDX and MDD). ***NOTE: For Python3 only!***

## Install

```shell script
pip install mdict-py
```

## Usage

**The API would be changed soon.**

```python
from mdict import MDD, MDX

mdx = MDX('example.mdx')

for item in mdx.items():
    headword, entry = item
    print(headword.decode('utf-8'))

mdd = MDD('example.mdd')

for item in mdd.items():
    filename, binary_contents = item
    print(filename)
```
