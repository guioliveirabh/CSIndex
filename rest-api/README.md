# CSIndex REST API

## Instructions

### [Create a virtual environment](https://docs.python.org/3/tutorial/venv.html)
```
$ python3.6 -m venv /path/to/new/virtual/environment
$ source </path/to/new/virtual/environment>/bin/activate
```

### Install the package
```
$ cd <CSIndex git repo>/rest-api
$ pip3 install -U pip setuptools wheel
$ pip3 install -e .[dev]
```

### Run the server
```
# to check the options
$ csi_server -h 

$ csi_server -d <CSIndex git repo>/data/
```

### Run the client
```
# to check the options
$ csi_client -h

$ csi_client
```

## ES2 Queries
1. Número de publicações em uma determinada conferência de uma área
   1. URL: http://{server}/conferences.{csv/json}/?area=se&name=SANER
1. Número de publicações no conjunto de conferências de uma área
   1. URL: http://{server}/areas.{csv/json}/?name=se
1. Scores de todos os departamentos em uma área
   1. URL: http://{server}/departments.{csv/json}/?area=se
1. Score de um determinado departamento em uma área.
   1. URL: http://{server}/departments.{csv/json}/?area=se&name=UFMG
1. Número de professores que publicam em uma determinada área (organizados por departamentos)
   1. URL: http://{server}/departments.{csv/json}/?area=se
1. Número de professores de um determinado departamento que publicam em uma área
   1. URL: http://{server}/departments.{csv/json}/?area=se&name=UFMG
1. Todos os papers de uma área (ano, título, deptos e autores)
   1. URL: http://{server}/papers.{csv/json}/?area=se
1. Todos os papers de uma área em um determinado ano
   1. URL: http://{server}/papers.{csv/json}/?area=se&year=2015
1. Todos os papers de um departamento em uma área
   1. URL: http://{server}/papers.{csv/json}/?area=se&department=UFMG
1. Todos os papers de um professor (dado o seu nome)
   1. URL: http://{server}/papers.{csv/json}/?researchers=Adenilso+Simao


## Full API documentation
The documentation is automatically generated and is available when the server is running 
in *http://{server}/docs* or in [docs](http://guilhermeoliveira.eti.br:8000/docs/).

There is a browsable API available when the server is running 
in *http://{server}/* or in [docs](http://guilhermeoliveira.eti.br:8000/)