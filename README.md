# ai-bank-operator

AI Bank Operator is a project designed to interact with customers using Generative AI models. This README provides instructions on how to set up and run the project.

## Prerequisites

- Docker
- Docker Compose
- Python 3.11
- Redis

## Setup

### 1. Clone the Repository

Clone the repository to your local machine using the following command:

```sh
git clone https://github.com/danielAdama/ai-bank-operator.git
```
```sh
cd ai-bank-operator
```
### 2. Create an Environment File
Create a .env file in the root directory of the project with the following command:
```sh
touch .env
```
After the creation of the .env, add the following environment variables:
```sh
GROQ_API_KEY=<your-groq-api-key>
OPENAI_API_KEY=<your-openai-api-key>
MODEL=<your-openai-model>
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
```
### 3. Docker Setup
Ensure Docker and Docker Compose are installed on your system. You can download Docker and Docker Compose from <https://docker-docs.uclv.cu/get-docker/>.
### 4. Build and Run the Project
Use the following command to build and run the project with Docker Compose:

```sh
docker-compose up -d
```
This command will build the Docker images and start the services defined in the docker-compose.yml file.
### 5. Access the Application
The application will be running at `http://localhost:80`.

### Project Structure
* src/: Contains the source code for the application.
* gen_ai/: Contains the AI models and utilities.
* utils/: Contains utility functions.
* config/: Configuration files for the project.
* Dockerfile: Dockerfile for building the Docker image.
* docker-compose.yml: Docker Compose configuration file.
* requirements.txt: Python dependencies.

### Makefile Commands
The project includes a Makefile with the following commands:

* compose_up: Runs Docker Compose to start the services.
* compose_down: Shuts down the Docker Compose services.
* start_dev: Runs the application in development mode.
* start_prod: Runs the application in production mode.
### API Endpoints
The application exposes the following API endpoints:

POST /v1/chat/messages/: Chat with the Large Language Model.
### Running the Application Locally
1. Install Dependencies
Ensure you have Python 3.11 installed. Then, install the dependencies using the following command:

```sh
python3 -m pip install --upgrade pip
```
```sh
pip3 install --no-cache-dir -r requirements.txt
```
2. Run the Application
Use the following command to run the application in development mode:

```sh
make start_dev
```
For production mode, use:

```sh
make start_prod
```
Contributing
Contributions are welcome! Please create a pull request with your changes.

License
This project is licensed under the MIT License.
