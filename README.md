# Sentiment Web Crawler

This is a web crawler developed for the final project of the fall 2018 COMP 479 - Information Retrieval course in Concordia University. The goal of the project is to experiment with web crawling, while scraping and indexing web documents and associating sentiment values to the index (using Afinn).

AFINN words can be downloaded [here](http://www2.imm.dtu.dk/pubdb/views/publication_details.php?id=6010). You can experiment with real-time sentiment analysis of words [here](https://darenr.github.io/afinn/).

## Getting Started

### Prerequisites

The following Python packages are required to run the program:

- [scrapy](https://scrapy.org/)
- [nltk](https://pypi.org/project/nltk/)
- [afinn](https://pypi.org/project/afinn/)
- [tabulate](https://pypi.org/project/tabulate/)

Click [here](requirements.txt) for the specific versions of the packages used for this project.

### Docker

A Dockerfile is included to make the script easier to run on any machine. First, make sure you `cd` into this repository.

To build the image and start up a container:

```
docker image build -t crawler .
docker container run -it --name crawler-demo crawler
```

This will take you to an interactive Bash terminal, from which you can [run](#running) the script. You can include the `--rm` option in the `run` command to automatically remove the container when you exit out of it.

### Running

The file to run is in the `src/` directory.

```
python main.py [-url|--start-url <"START_URL">]
               [-ign|--ignore-robots]
               [-m|--max <MAX>]
               [-rs|--remove-stopwords]
               [-nf|--no-follow]
               [-wiki|--wikipedia-only]

optional arguments:
    -url, --start-url               set URL the crawler will start from, (default https://www.concordia.ca/about.html)
    -ign, --ignore-robots           the crawler will not respect robot exclusion
    -m, --max                       set maximum number of pages to scrape (default 10)
    -rs, --remove-stopwords         remove stopwords from the index
    -nf, --no-follow                do not follow extracted links
    -wiki, --wikipedia-only         the crawler will only crawl English Wikipedia articles
    -skip, --skip-crawl             skip crawl, use index from most recent run
```

Surround the `-url` option's value with double quotes for best results.

If you intend to use `-skip`, no need to specify the other options. You would obviously need to have run the crawler first, to generate a data set. Simply run:

```
python main.py [-skip|--skip-crawl]
```

## Authors

- **François Crispo-Sauvé** - *ID:* 27454139
- **Roger Shubho Madhu** - *ID:* 40076461
- **Vartan Benohanian** - *ID:* 27492049

## Report

The project report, which includes more detailed specifications, as well as sample runs of the application, can be viewed [here](Project%20Report.pdf).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
