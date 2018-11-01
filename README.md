# TCP-UDP-protocol
This project implements a based TCP protocol with Go Back N using UDP under the hood.

## Server mode usage 
```
$ make runserver
```
or 
```
$ python server.py
```

## Client mode usage 
```
$ python client.py <file_to_send> # to default address defined in conf.py
```
or 
```
$ python client.py <file_to_send> <ip_address> <port> # optional
```
