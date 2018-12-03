FROM python:3

RUN mkdir -p /usr/app
WORKDIR /usr/app

COPY requirements.txt /usr/app

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

COPY src /usr/app/src
WORKDIR /usr/app/src

CMD ["bash"]
