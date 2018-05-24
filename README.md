# moodle-spider

moodle-spider is a small Python script for downloading all available files from moodle

It downloads all available files from all open courses in moodle. Before downloading file, it checks if file already exists (no duplicates are made).

## Installation

### Requirements
* Linux/macOS
* Python 2.6+ (no Python 3 support currently)
* mechanize, BeautifulSoup4 python libraries

## Usage
1. Clone this repository
```
$ git clone http://github.com/mannyfm/moodle-spider
```

2. Install required dependencies
```
$ pip install -r requiremnets.txt
```

3. You need make a config file, you can use `config.sample.ini` as example
```
$ cp config.sample.ini config.ini
```

4. Make sure output directory exists. (We assume it is `output`)
```
$ mkdir output
```

5. Run Spider
```
$ python spider.py
```

## TODO
- [x] Basic file download
- [x] Redirect file download
- [x] Folder download
- [ ] Assignment attachments download
- [ ] Make downloads asynchronous

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Authors

* **Alibek Manabayev** -  [MannyFM](https://github.com/MannyFM)

This code is modified and extended version of [`moodle-downloader`](https://github.com/vinaychandra/Moodle-Downloader) by [Vinay Chandra](https://github.com/vinaychandra/).
## License
[MIT](https://choosealicense.com/licenses/mit/)
