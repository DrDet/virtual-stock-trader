# vstrader
FastAPI python backend for virtual stock trading

## Setup
At first, you need to install dependencies specified in `requirements.txt`:
```
pip install -r requirements.txt 
```
## Run tests
To run all tests just call from the root:
```
PYTHONPATH=. pytest
```
Also, it's possible to run a specific test group:
```
PYTHONPATH=. pytest tests/unit-tests         # to run unit tests
PYTHONPATH=. pytest tests/integration-tests  # to run integration tests
```
