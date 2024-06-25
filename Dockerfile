FROM python:3.11

ARG REDIS_DB \
    REDIS_HOST \
    REDIS_PORT \
    GROQ_API_KEY \
    OPENAI_API_KEY \
    MODEL

ENV REDIS_DB: ${REDIS_DB} \
    REDIS_HOST: ${REDIS_HOST} \
    REDIS_PORT: ${REDIS_PORT} \
    GROQ_API_KEY: ${GROQ_API_KEY} \
    OPENAI_API_KEY: ${OPENAI_API_KEY} \
    MODEL: ${MODEL}

WORKDIR /app

COPY . .

RUN python3 -m pip install --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT ["make", "start_prod"]