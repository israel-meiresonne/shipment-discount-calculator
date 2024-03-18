# Shipment discount calculator

Module to calculate shipment price for a given transaction and history.

## Technologies

* Python 3.12.0 (no dependencies)
* Docker

## UML Class Diagram

[<img src="./docs/rsc/final-class-diagram.drawio.svg" width="500">](./docs/rsc/final-class-diagram.drawio.svg)

## Run without Docker

1. Clone the project

    ```Shell
    git clone https://github.com/israel-meiresonne/shipment-discount-calculator.git
    ```

2. Change your directory to the source code

    ```Shell
    cd ./src
    ```

3. Run the Python main code

    ```Shell
    python main.py input.txt
    ```

4. Run the Python tests

    ```Shell
    python tests.py
    ```

## Run with Docker

1. Clone the project

    ```Shell
    git clone https://github.com/israel-meiresonne/shipment-discount-calculator.git
    ```

2. Start Python service from Docker-compose

    ```Shell
    docker-compose up python-3.12.0 -d
    ```

3. Run the Python main code

    ```Shell
    docker exec python-shipment python main.py input.txt
    ```

4. Run the Python tests

    ```Shell
    docker exec python-shipment python test.py
    ```

5. Shut down the Python service

    ```Shell
    docker-compose down python-3.12.0
    ```
