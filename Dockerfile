FROM python:3

RUN mkdir -p /usr/src
WORKDIR /usr/src

COPY requirements.txt /usr/src

RUN pip install --no-cache-dir -r requirements.txt && \
    python -m nltk.downloader punkt && \
    python -m nltk.downloader stopwords

RUN echo "alias ..='cd ..'" >> ~/.bashrc && \
    echo "alias ...='cd ../..'" >> ~/.bashrc && \
    echo "alias ....='cd ../../..'" >> ~/.bashrc && \
    echo "alias grep='grep --colour=auto'" >> ~/.bashrc && \
    echo "alias l='ls -ltr'" >> ~/.bashrc && \
    echo "alias ll='ls -ltr'" >> ~/.bashrc && \
    echo "alias cl='clear'" >> ~/.bashrc

COPY src /usr/src/app
WORKDIR /usr/src/app

CMD ["bash"]
