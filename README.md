# Generate a signing key

Generate a signing key by requesting a binary blob from random.org. Requires a random.org API key.

The random.org python client `rdoclient-py3` could be used. However, it does not run on Python 3.8 or later. 
The module uses`time.clock()` which was deprecated in Python 3.3.


## credentials file
Save the random.org API key in a JSON file with the following stricture.
```json
{
  "api_key": "11111111-2222-3333-4444-555555555555"
}
```
## ToDo 
* requirements file

```bash
    python -m venv venv
    pip install requests
```

