# AI Bank Operator

A customer-facing banking assistant that answers customers using generative AI models. It runs as an API with Redis alongside it and starts with a single Docker Compose command.

## Features

- Chat endpoint for customer conversations, backed by OpenAI or Groq models
- Redis service included in the Docker Compose setup
- Development and production run modes
- Containerised with Docker and Docker Compose

## Built with

Python 3.11 · OpenAI · Groq · Redis · Docker

## Quick start with Docker

### Prerequisites

- [Docker and Docker Compose](https://docs.docker.com/get-docker/)
- An OpenAI API key and a Groq API key

### 1. Clone the repository

```bash
git clone https://github.com/danielAdama/ai-bank-operator.git
cd ai-bank-operator
```

### 2. Add your environment variables

Create a `.env` file in the project root with:

```bash
GROQ_API_KEY=<your-groq-api-key>
OPENAI_API_KEY=<your-openai-api-key>
MODEL=<your-openai-model>
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
```

### 3. Start it

```bash
docker-compose up -d
```

This builds the images and starts every service in `docker-compose.yml`, including Redis. The app is then available at http://localhost:80.

To stop it:

```bash
docker-compose down
```

## Run locally without Docker

You need Python 3.11 and a Redis server running on your machine. Set `REDIS_HOST=localhost` in your `.env`.

```bash
python3 -m pip install --upgrade pip
pip3 install --no-cache-dir -r requirements.txt

make start_dev     # development mode
make start_prod    # production mode
```

## API

| Method | Endpoint | What it does |
|---|---|---|
| `POST` | `/v1/chat/messages/` | Sends a customer message and returns the assistant's reply |

## Makefile commands

| Command | What it does |
|---|---|
| `make compose_up` | Start the services with Docker Compose |
| `make compose_down` | Stop the services |
| `make start_dev` | Run the app in development mode |
| `make start_prod` | Run the app in production mode |

## Project structure

```
ai-bank-operator/
├── src/                 # Application source code
├── gen_ai/              # AI models and utilities
├── config/              # Configuration
├── Dockerfile
├── docker-compose.yml
├── Makefile
└── requirements.txt
```

## Contributing

Contributions are welcome. Open a pull request with your changes.

## License

MIT. See [LICENSE](LICENSE).

## Contact

Daniel Enemona Adama · [adamadaniel321@gmail.com](mailto:adamadaniel321@gmail.com) · [Portfolio](https://daniel-adama.vercel.app)
