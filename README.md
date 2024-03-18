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
    cd ./shipment-discount-calculator/src
    ```

3. Run the Python main code

    ```Shell
    python main.py input.txt
    ```

4. Run the Python tests

    ```Shell
    python test.py
    ```

## Run with Docker

1. Clone the project

    ```Shell
    git clone https://github.com/israel-meiresonne/shipment-discount-calculator.git
    ```

2. Change your directory to the cloned project

    ```Shell
    cd ./shipment-discount-calculator
    ```

3. Start Python service from Docker-compose

    ```Shell
    docker-compose up python-3.12.0 -d
    ```

4. Run the Python main code

    ```Shell
    docker exec python-shipment python main.py input.txt
    ```

5. Run the Python tests

    ```Shell
    docker exec python-shipment python test.py
    ```

6. Shut down the Python service (optional)

    ```Shell
    docker-compose down python-3.12.0
    ```

7. Destroy the Python image used by Docker (optional)

    ```Shell
    docker image rm shipment-discount-calculator-python-3.12.0
    ```
