# Discogs Python API Wraper

This is a python API wrapper for the discogs API.

## Installation 

## Quickstart

```bash
from discogs_wrapper import DV

dv_instance = DV("FooBarApp/3.0")
response = dv_instance.get_search(genre='rock',q = 'nirvana',token='abcde123')
```

