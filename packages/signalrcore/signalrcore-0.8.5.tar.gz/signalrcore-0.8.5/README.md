# SignalR core client
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg?logo=paypal&style=flat-square)](https://www.paypal.me/mandrewcito/1)
![Pypi](https://img.shields.io/pypi/v/signalrcore.svg)
![Pypi - downloads month](https://img.shields.io/pypi/dm/signalrcore.svg)
![Issues](https://img.shields.io/github/issues/mandrewcito/signalrcore.svg)
![Open issues](https://img.shields.io/github/issues-raw/mandrewcito/signalrcore.svg)


![logo alt](https://raw.githubusercontent.com/mandrewcito/signalrcore/master/docs/img/logo_temp.128.svg.png)


# Links 

* [Dev to posts with library examples and implementation](https://dev.to/mandrewcito/singlar-core-python-client-58e7)

* [Pypy](https://pypi.org/project/signalrcore/)

* [Wiki - This Doc](https://mandrewcito.github.io/signalrcore/)

# A tiny How To

## Connect to a server without auth
```python
hub_connection = HubConnectionBuilder()\
    .with_url(server_url)\
    .configure_logging(logging.DEBUG)\
    .with_automatic_reconnect({
        "type": "raw",
        "keep_alive_interval": 10,
        "reconnect_interval": 5,
        "max_attempts": 5
    }).build()
```
## Connect to a server with auth

login_function must provide auth token

```python
hub_connection = HubConnectionBuilder()\
            .with_url(server_url,
            options={
                "access_token_factory": login_function,
                "headers": {
                    "mycustomheader": "mycustomheadervalue"
                }
            })\
            .configure_logging(logging.DEBUG)\
            .with_automatic_reconnect({
                "type": "raw",
                "keep_alive_interval": 10,
                "reconnect_interval": 5,
                "max_attempts": 5
            }).build()
```
## Configure logging

```python
HubConnectionBuilder()\
    .with_url(server_url,
    .configure_logging(logging.DEBUG)
    ...
```
## Configure socket trace
```python 
HubConnectionBuilder()\
    .with_url(server_url,
    .configure_logging(logging.DEBUG, socket_trace=True) 
    ... 
 ```
 ## Configure your own handler
 ```python
 import logging
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
hub_connection = HubConnectionBuilder()\
    .with_url(server_url, options={"verify_ssl": False}) \
    .configure_logging(logging.DEBUG, socket_trace=True, handler=handler)
    ...
 ```
## Configuring reconection
After reaching max_attemps an exeption will be thrown and on_disconnect event will be
fired.
```python
hub_connection = HubConnectionBuilder()\
    .with_url(server_url)\
    ...
    .build()
```
## Configuring aditional headers
```python
hub_connection = HubConnectionBuilder()\
            .with_url(server_url,
            options={
                "headers": {
                    "mycustomheader": "mycustomheadervalue"
                }
            })
            ...
            .build()
```
## Configuring aditional querystring parameters
```python
server_url ="http.... /?myquerystringparam=134&foo=bar"
connection = HubConnectionBuilder()\
            .with_url(server_url,
            options={
            })\
            .build()
```
## Congfigure skip negotiation
```python
hub_connection = HubConnectionBuilder() \
        .with_url("ws://"+server_url, options={
            "verify_ssl": False,
            "skip_negotiation": False,
            "headers": {
            }
        }) \
        .configure_logging(logging.DEBUG, socket_trace=True, handler=handler) \
        .build()

```
## Configuring ping(keep alive)

keep_alive_interval sets the secconds of ping message

```python
hub_connection = HubConnectionBuilder()\
    .with_url(server_url)\
    .configure_logging(logging.DEBUG)\
    .with_automatic_reconnect({
        "type": "raw",
        "keep_alive_interval": 10,
        "reconnect_interval": 5,
        "max_attempts": 5
    }).build()
```
## Configuring logging
```python
hub_connection = HubConnectionBuilder()\
    .with_url(server_url)\
    .configure_logging(logging.DEBUG)\
    .with_automatic_reconnect({
        "type": "raw",
        "keep_alive_interval": 10,
        "reconnect_interval": 5,
        "max_attempts": 5
    }).build()
```
## Events

### On connect / On disconnect
on_open - fires when connection is openned and ready to send messages
on_close - fires when connection is closed
```python
hub_connection.on_open(lambda: print("connection opened and handshake received ready to send messages"))
hub_connection.on_close(lambda: print("connection closed"))

```
### Register an operation 
ReceiveMessage - signalr method
print - function that has as parameters args of signalr method
```python
hub_connection.on("ReceiveMessage", print)
```
## Sending messages
SendMessage - signalr method
username, message - parameters of signalrmethod
```python
    hub_connection.send("SendMessage", [username, message])
```
## Requesting streaming (Server to client)
```python
hub_connection.stream(
            "Counter",
            [len(self.items), 500]).subscribe({
                "next": self.on_next,
                "complete": self.on_complete,
                "error": self.on_error
            })
```
## Client side Streaming
```python
from signalrcore.subject import  Subject

subject = Subject()

# Start Streaming
hub_connection.send("UploadStream", subject)

# Each iteration
subject.next(str(iteration))

# End streaming
subject.complete()




```
# Full Examples

Using package from [aspnet core - SignalRChat](https://codeload.github.com/aspnet/Docs/zip/master) 
example chat without auth
```python

from signalrcore.hub_connection_builder import HubConnectionBuilder


def input_with_default(input_text, default_value):
    value = input(input_text.format(default_value))
    return default_value if value is None or value.strip() == "" else value


server_url = input_with_default('Enter your server url(default: {0}): ', "ws://localhost:62342/chathub")
username = input_with_default('Enter your username (default: {0}): ', "mandrewcito")

hub_connection = HubConnectionBuilder().with_url(server_url).with_automatic_reconnect({
        "type": "raw",
        "keep_alive_interval": 10,
        "reconnect_interval": 5,
        "max_attempts": 5
    }).build()
hub_connection.on("ReceiveMessage", print)
hub_connection.start()
message = None
# Do login

while message != "exit()":
    message = input(">> ")
    if message is not None and message is not "" and message is not "exit()":
        hub_connection.send("SendMessage", [username, message])
hub_connection.stop()


```

Using package from [aspnet core - SignalRAuthenticationSample](https://codeload.github.com/aspnet/Docs/zip/master) ,

# Example with Auth
```python
import requests
from signalrcore.hub_connection_builder import HubConnectionBuilder


def input_with_default(input_text, default_value):
    value = input(input_text.format(default_value))
    return default_value if value is None or value.strip() == "" else value


def signalr_core_example_login(url, user, username_password):
    response = requests.post(url, data={"email": user, "password": username_password})
    return response.json()["token"]


login_url = input_with_default('Enter your server login url({0}):', "http://localhost:50746/account/token")
server_url = input_with_default('Enter your server url(default: {0}): ', "ws://localhost:50746/hubs/chat")
username = input_with_default('Enter your username (default: {0}): ', "mandrewcito@mandrewcito.com")
password = input_with_default('Enter your password (default: {0}): ', "Abc123.--123?")

hub_connection = HubConnectionBuilder()\
    .with_url(server_url, options={
        "access_token_factory": lambda: signalr_core_example_login(login_url, username, password)
    }).with_automatic_reconnect({
        "type": "interval",
        "keep_alive_interval": 10,
        "intervals": [1, 3, 5, 6, 7, 87, 3]
    })\
    .build()

hub_connection.on("ReceiveSystemMessage", print)
hub_connection.on("ReceiveChatMessage", print)
hub_connection.on("ReceiveDirectMessage", print)
hub_connection.start()
message = None
while message != "exit()":
    message = input(">> ")
    if message is not None and message is not "" and message is not "exit()":
        hub_connection.send("Send", [message])
hub_connection.stop()
```
# Example with streaming

Using package from [aspnet core - SignalRStreaming](https://codeload.github.com/aspnet/Docs/zip/master) ,

```python


import time
import sys
from signalrcore.hub_connection_builder import HubConnectionBuilder


def input_with_default(input_text, default_value):
    value = input(input_text.format(default_value))
    return default_value if value is None or value.strip() == "" else value


server_url = input_with_default('Enter your server url(default: {0}): ', "ws://localhost:57957/streamHub")

hub_connection = HubConnectionBuilder().with_url(server_url).build()
hub_connection.start()
time.sleep(10)


def bye(error, x):
    if error:
        print("error {0}".format(x))
    else:
        print("complete! ")
    global hub_connection
    hub_connection.stop()
    sys.exit(0)


hub_connection.stream(
    "Counter",
    [10, 500]).subscribe({
        "next": lambda x: print("next callback: ", x),
        "complete": lambda x: bye(False, x),
        "error": lambda x: bye(True, x)
    })

```

# Example with client side streaming

Using package from [aspnet core - SignalRStreaming](https://docs.microsoft.com/es-es/aspnet/core/signalr/streaming?view=aspnetcore-3.1) ,



````python
from signalrcore.hub_connection_builder import HubConnectionBuilder
from signalrcore.subject import Subject


def input_with_default(input_text, default_value):
    value = input(input_text.format(default_value))
    return default_value if value is None or value.strip() == "" else value


server_url = input_with_default('Enter your server url(default: {0}): ', "wss://localhost:44376/chatHub")

hub_connection = HubConnectionBuilder()\
    .with_url(server_url, options={"verify_ssl": False}) \
    .configure_logging(logging.DEBUG) \
    .with_automatic_reconnect({
            "type": "interval",
            "keep_alive_interval": 10,
            "intervals": [1, 3, 5, 6, 7, 87, 3]
        })\
    .build()
hub_connection.start()
time.sleep(10)


def bye(error, x):
    if error:
        print("error {0}".format(x))
    else:
        print("complete! ")
    global hub_connection
    hub_connection.stop()
    sys.exit(0)


iteration = 0
subject = Subject()


def interval_handle():
    global iteration
    iteration += 1
    subject.next(str(iteration))
    if iteration == 10:
        subject.complete()


hub_connection.send("UploadStream", subject)

while iteration != 10:
    interval_handle()
    time.sleep(0.5)

````

# Example azure functions

Using this [example](https://docs.microsoft.com/es-es/azure/azure-signalr/signalr-quickstart-azure-functions-javascript?WT.mc_id=signalrquickstart-github-antchu) ,

```python
import logging
import sys
import requests
from signalrcore.hub_connection_builder import HubConnectionBuilder


def input_with_default(input_text, default_value):
    value = input(input_text.format(default_value))
    return default_value if value is None or value.strip() == "" else value


server_url = input_with_default(
    'Enter your server url(default: {0}): ',
    "localhost:7071/api")
username = input_with_default('Enter your username (default: {0}): ', "mandrewcito")
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
hub_connection = HubConnectionBuilder() \
        .with_url("ws://"+server_url, options={
            "verify_ssl": False,
            "skip_negotiation": False,
            "headers": {
            }
        }) \
        .configure_logging(logging.DEBUG, socket_trace=True, handler=handler) \
        .build()

hub_connection.on_open(lambda: print("connection opened and handshake received ready to send messages"))
hub_connection.on_close(lambda: print("connection closed"))

hub_connection.on("newMessage", print)
hub_connection.start()
message = None

# Do login

while message != "exit()":
    message = input(">> ")
    if message is not None and message is not "" and message is not "exit()":
        # hub_connection.send("sendMessage", [username, message])
        requests.post("http://localhost:7071/api/messages", json={"sender": username, "text": message})

hub_connection.stop()

sys.exit(0)

```