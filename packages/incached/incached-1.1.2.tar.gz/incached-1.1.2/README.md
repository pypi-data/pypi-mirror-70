# incached

[![pipeline status](https://gitlab.com/cytedge/incached/badges/master/pipeline.svg)](https://gitlab.com/cytedge/incached/-/commits/master)
**Ultimate cache engine for Python3**

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install incached.

```bash
pip install incached
```

## Usage

```python
import incached

inc = incached.INCached(cachesize=0)  # Set cachesize to infinite
```
```python
def fibonacci(num):  # Example fibonacci without caching, try to run it
	if num < 2:
		return num
	return fibonacci(num-1)+fibonacci(num-2)
	
fibonacci(40)  # After 35 iterations, the performance will slow down considerably.
```
```python
def cached_fibonacci(num):  # Example fibonacci with caching
	if num < 2:
		return num
	return inc.cache(cached_fibonacci, (num-1,))+inc.cache(cached_fibonacci, (num-1,))  # Explanation below
```
```python
inc.cache(cached_fibonacci, (40,))  # Arguments is the function without calling, and the tuple with the arguments.
```
Try changing 40 to 400, the calculations are almost instantaneous compared to the non-cached function.
```python
>>> print(inc.cache_info())  # Prints cache info
{'hits': 399, 'misses': 400, 'cachesize': 400}
>>> inc.save_cache("test.cache", save_stats=True)  # Save cache to file
>>> inc.clear_cache()  # Clear the cache
>>> inc.clear_stats()  # Clear hits and misses
>>> inc.load_cache("test.cache", load_stats=True)  # Load cache from file
```
Utils:
```python
>>> from incached import utils
>>> utils.save_full_cache("test.full", inc)  # Fully save cache to file
>>> x = utils.load_full_cache("test.full")  # Load full cache from file
>>> print(inc.cache_info())  # Prints cache info
{'hits': 399, 'misses': 400, 'cachesize': 400}
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)