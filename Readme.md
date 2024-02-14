# Command line LSB webscraper.

This is a simple command line tool that scrapes user requested bible verses from read.lsbible.org. You can get single verses, multiple verses, or whole chapters. Can be easily compiled into a single binary with pyinstall.

## Requirements
* Python 3
* bs4
* requests

## Usage
For a single verse
```
python lsb.py Romans 13:10
```

Whole chapters (no more than a single chapter)

```
python lsb.py Psalm 23
```
In the case of single chapter books (other books will give the first chapter)
```
python lsb.py Obadiah
```