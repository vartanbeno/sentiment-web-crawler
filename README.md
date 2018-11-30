# Sentiment Web Crawler

This is a web crawler developed for the final project of the fall 2018 COMP 479 - Information Retrieval course in Concordia University. The goal of the project is to experiment with web crawling, while scraping and indexing web documents and associating sentiment values to the index (using Afinn).

The start URL is the [about page](https://www.concordia.ca/about.html) of the Concordia University website.

AFINN words can be downloaded [here](http://www2.imm.dtu.dk/pubdb/views/publication_details.php?id=6010). You can experiment with real-time sentiment analysis of words [here](https://darenr.github.io/afinn/).

## Getting Started

### Prerequisites

The following Python packages are required to run the program:

- [scrapy](https://scrapy.org/)
- [nltk](https://pypi.org/project/nltk/)
- [afinn](https://pypi.org/project/afinn/)

Click [here](requirements.txt) for the specific versions of the packages used for this project.

### Docker

A Dockerfile is included to make the script easier to run on any machine. First, make sure you `cd` into this repository.

To build the image and start up a container:

```
docker image build -t crawler .
docker container run -it --name crawler-demo crawler bash
```

This will take you to an interactive Bash terminal, from which you can [run](#running) the script. You can include the `--rm` option in the `run` command to automatically remove the container when you exit out of it.

### Running

The file to run is in the root directory of the project.

```
python main.py [-l LIMIT]
```

The arguments are the following:

1. `-l` or `--limit`: maximum number of links to scrape. Default is 10.

## Authors

- **François Crispo-Sauvé** - *ID:* 27454139
- **Roger Shubho Madhu** - *ID:* 40076461
- **Vartan Benohanian** - *ID:* 27492049

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
