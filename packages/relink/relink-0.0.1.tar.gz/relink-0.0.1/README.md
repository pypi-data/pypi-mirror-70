relink
========

A client for https://rel.ink/ API

## Installation

```
$ pip install relink
````

## Usage

```
from relink.client import RelinkClient

client = RelinkClient()

shortened_url = client.shorten_url("https://news.ycombinator.com/")
print(shortened_url) # => 'https://rel.ink/Nn8y9p'

client.get_full_url(shortened_url) # => "https://news.ycombinator.com/"
```

## License

relink is licensed under the Apache 2.0 license.
