FROM rocker/r-ver:3.5.1

LABEL maintainer="Nancy Irisarri Mendez <nancyirisarri@gmail.com>"

# TODO Install R dependencies

# TODO Install Python and dependencies

COPY pyladies.amsterdam.etl /src

RUN mkdir -p /nonexistent/.ssh && \
    chown -R nobody.nogroup /src/ /nonexistent/.ssh/

USER nobody

CMD ["python3", "-m", "src.main"]

