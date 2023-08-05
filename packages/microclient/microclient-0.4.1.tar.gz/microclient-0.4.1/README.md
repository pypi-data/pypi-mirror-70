# Microclient
Microclient is a library for building simple python clients for your microservices.

Basic usage:
```python
from microclient import BaseClient, EndpointInfo

class ZOOClient(BaseClient):
    service_name = 'ZOO API'
    base_url = 'http://localhost:8000'
    endpoints = [
        EndpointInfo("animals", [
            EndpointInfo("cats", "GET"),
            EndpointInfo("dogs", "GET"),
            EndpointInfo("elephants", "GET"),
        ]),
        EndpointInfo("zoo-status", "GET"),
        EndpointInfo("tickets", "GET, POST, DELETE")
    ]
```

Which translates into client like this:
```python
zoo_client = ZooClient()
zoo_client.animals.cats() # sends GET request to http://localhost:8000/animals/cats
zoo_client.tickets.post(data={'amount': 2})  # sends POST request to http://localhost:8000/tickets with json data
```

Currently microclient is working with json data only (requests and responses).