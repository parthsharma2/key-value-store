# KVS - Key Value Store
A REST API based Key Value Store.

## Getting Started
These instructions wil get you a copy of the project up and
running on your local machine for development and testing purposes.

### Requirements

- `python3.6+`

### Installing

Clone the project.
```bash
git clone https://github.com/parthsharma2/key-value-store.git
```

Move into the project directory.
```bash
cd key-value-store
```

Create a python virtual environment and activate it.
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install python dependencies.
```bash
pip install -r requirements.txt
```


## Usage
KVS can be used via REST API or a CLI.

### Starting the server
Use the following command to start the KVS REST API server.
```bash
python -m kvs.server
```
This will start the server on the default host `127.0.0.1` and port `25552`.
To run it on a custom host and port use the following command
```bash
python -m kvs.server -H 127.0.0.1 -p 25252
```
or
```bash
python -m kvs.server --host=127.0.0.1 --port=25252
```

### Starting the client
Use the following command to start the KVS Client. Make sure the
KVS REST API server is running.
```bash
python -m kvs.client
```
This will start the client and try to connect with a KVS REST API
server running on host `127.0.0.1` and port `25552`.
If your KVS REST API server is running on a different host and/or port use
the following commands.
```bash
python -m kvs.client -H 127.0.0.1 -p 25252
```
or
```bash
python -m kvs.client --host=127.0.0.1 --port=25252
```

### API Endpoints
The following REST API endpoints are available:

| Endpoint      | HTTP Method     | Description       |
|---------------|-----------------|-------------------|
|`/api/<key>`   | `GET`           | Gets the value of the key `<key>`. Returns `null` if the key does not exist.|
|`/api/<key>`   | `POST`          | Sets the value of the key `<key>` to the value specified in the posted json data. The data to be posted should be a json key value pair of the format `{"value": "some value"}`. A successful POST request will set the value of `<key>` to the value specified by `"value"` in the posted json data.|
|`/api/<key>`   | `DELETE`        | Deletes the key value pair specified by `<key>`|
|`/api/ping`    | `GET`           | Gets the status of the server.|

### CLI Commands
In the client the following CLI commands are available:

| Command           | Description       |
|-------------------|-------------------|
|`get <key>`        | Get the value of the key `<key>`. Returns `null` if the key does not exist. |
|`set <key> <value>`| Set the value of the key `<key>` to `<value>`.|
|`delete <key>`     | Deletes the key value pair specified by `<key>`.|
|`exit`             | Quits and closes the client.|


## Examples

### REST API
Make sure the REST API server is running.

We'll use `curl` to send HTTP requests to the KVS REST API server.
```bash
# Check status of the server
curl -i http://localhost:25552/api/ping

# Let's try and get key "hello" value
curl -i http://localhost:25552/api/hello
# We get "null" because the value of hello is not set

# Let's set the value of "hello" to "world"
curl -i -d '{"value":"world"}' -H "Content-Type: application/json" -X POST http://localhost:25552/api/hello

# Now let's again try to get the value of "hello"
curl -i http://localhost:25552/api/hello
# This time we get the value "world"

# Let's delete the key "hello"
curl -i -X DELETE http://localhost:25552/api/hello

# Just to check if "hello" is deleted let's try to get it
curl -i http://localhost:25552/api/hello
# We get "null"
```
### CLI Commands
Make sure the REST API server is running and start the client.

In the client shell use the following commands:
```bash
# Get the value of key "hello"
get hello

# Set the value of "hello" to "world"
set hello world

# Get the value of key "hello"
get hello

# Delete the key "hello"
delete hello

# Get the value of "hello"
get hello

# Exit the client
exit
```

## Running the Tests
To run the tests use the following command while in the project root directory:
```
pytest tests/
```