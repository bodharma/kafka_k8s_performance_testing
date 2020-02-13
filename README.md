### Kafka Kubernetes Performance Testing

Is used to post messages to Kafka with predefined speed 50 messages per second.


To start the one container with simulator, use docker-compose from the project root directory:

```bash
docker-compose build producer-local
docker-compose up producer-local

```

##### How to setup the project for local demo:

1. Clone this repo
2. Go to terminal and run
    ```bash
    docker-compose up local-producer 
    ```
3. Go to terminal and run
    ```bash
    docker-compose up local-consumer
    ```
4. Enjoy


##### How to setup the project for development:

1. Install (pipenv)[https://pypi.org/project/pipenv]
2. Create venv
    ```bash
    pipenv shell
    ```
3. Start working

##### How to run on k8s
1. TBD
