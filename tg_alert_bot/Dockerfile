FROM python:3.12

WORKDIR /tg_bot

RUN apt update --no-install-recommends -y && \
    apt install -y tzdata locales && \
    rm -rf /var/lib/apt/lists/*

RUN sed -i '/^# en_/s/^# //' /etc/locale.gen && \
    sed -i '/^# ru_/s/^# //' /etc/locale.gen && \
    locale-gen

ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8

ENV TZ=Europe/Moscow
RUN ln -fs /usr/share/zoneinfo/Europe/Moscow /etc/localtime && dpkg-reconfigure --frontend=noninteractive tzdata

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.8.3

RUN pip install "poetry==$POETRY_VERSION"

COPY poetry.lock .
COPY pyproject.toml .

RUN poetry config virtualenvs.create false \
    && poetry install  --no-root

COPY . .

CMD ["python3", "main.py"]
