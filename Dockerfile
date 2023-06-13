FROM python:3.11

COPY --chmod=+x entrypoint.sh /entrypoint.sh

RUN groupadd -g 1000 jenkins
RUN useradd -g jenkins -m jenkins

WORKDIR /src

USER jenkins

ENTRYPOINT ["/entrypoint.sh"]
