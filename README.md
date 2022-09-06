# Czech Elections 2021 shell data feed

Fetches data from the Czech Statistical Office Open data server, parses them and outputs them into the console. 

API calls are disk-cached for 1 minute. Shell content "reload" is set for 1 minute as well.

## Dependencies

- Python 3.9 - developed and tested, but should work probably on 3.6+
- pipenv - to smooth handle the packages installation

### Installation

1. Clone the repository
2. In the root of the project run `pipenv shell` then `pipenv install`.
3. In case the `run.py` will throw due to import errors, run also `python setup.py develop`.


### How to run

1. To get county data for given NUTS (see Czech Statistical Office classifiers in `/src/classifiers/nuts.csv`):

    ```
    python run.py county CZ0100
    ```

2. To get county data for given NUTS and specific city belonging to the NUTS:

    ```
    python run.py county CZ0100 --name "Praha 1"
    ```

    `--name` parameter is case sensitive.

3. To get state data:

    ```
    python run.py state
    ```

4. To get data for specific state district (e.g. North Moravian-Silesian):

    ```
    python run.py state --district 14
    ```

Execution is terminated by simply pressing `CTRL+C`.
