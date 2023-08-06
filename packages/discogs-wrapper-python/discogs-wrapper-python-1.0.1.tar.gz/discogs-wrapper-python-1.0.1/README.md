# Discogs Python API Wraper

This is a python API wrapper for the discogs API. It includes methods for API endpoints in the Database section in discogs.

## Installation 

```bash
pip install discogs-wrapper-python
```

## Quickstart

```bash
from discogs_wrapper import DV

dv_instance = DV("FooBarApp/3.0")
response = dv_instance.get_search(genre='rock',q = 'nirvana',token='abcde123')
```

## Authentication
There are two primary methods of authentication: Discogs Auth Flow and Auth Flow. As of now, only Discogs Auth Flow is supported by this wrapper. This is a simple yet secure way of authenticating a user. A user can be authenticated either by using a __User token__ or using a __Consumer key__ and __secret__. 

