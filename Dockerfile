FROM python:3-onbuild

RUN echo "alias ..='cd ..'" >> ~/.bashrc && \
    echo "alias ...='cd ../..'" >> ~/.bashrc && \
    echo "alias ....='cd ../../..'" >> ~/.bashrc && \
    echo "alias grep='grep --colour=auto'" >> ~/.bashrc && \
    echo "alias l='ls -ltr'" >> ~/.bashrc && \
    echo "alias ll='ls -ltr'" >> ~/.bashrc && \
    echo "alias cl='clear'" >> ~/.bashrc

RUN python -m nltk.downloader punkt && \
    python -m nltk.downloader stopwords

WORKDIR /usr/src/app/src

CMD ["bash"]
