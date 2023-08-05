# danksearch

danksearch is an async library to search youtube without using any API's.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install danksearch.

```bash
pip install danksearch
```

## Usage

```python
import danksearch, asyncio

async def searchvideo():
    video=danksearch.Video()
    await video.search("spooky scary skeletons")
    print(video.url)

asyncio.run(searchvideo())

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://github.com/actualdankcoder/danksearch-discord/blob/master/LICENSE)