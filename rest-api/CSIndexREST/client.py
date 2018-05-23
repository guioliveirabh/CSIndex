import argparse
from pprint import pprint

import requests


class APIRequestData:
    BASE_URL = 'http://{server}:{port}/{data_type}.{output_type}'
    CSV_OUTPUT = 'csv'
    JSON_OUTPUT = 'json'

    def __init__(self, server, port, data_type, output_type, parameters=None):
        self.data_type = data_type
        self.output_type = output_type
        self.parameters = parameters
        self.port = port
        self.server = server

    def get_url(self):
        return self.BASE_URL.format(server=self.server,
                                    port=self.port,
                                    data_type=self.data_type,
                                    output_type=self.output_type)

    def print_output(self):
        print('URL: {0}'.format(self.get_url()))
        if self.parameters:
            print('PARAMETERS: {0}'.format(self.parameters))
        print('DATA:\n')
        request = requests.get(url=self.get_url(), params=self.parameters)
        if self.output_type == self.CSV_OUTPUT:
            print(request.text)
        elif self.output_type == self.JSON_OUTPUT:
            pprint(request.json(), width=160, indent=2)


def parse_args():
    parser = argparse.ArgumentParser(description='CSIndex REST API client')
    parser.add_argument('-i', '--ip', metavar='IP', default='guilhermeoliveira.eti.br', help='the server name/IP')
    parser.add_argument('-p', '--port', metavar='PORT', type=int, default='8000', help='the server port')
    parser.add_argument('-o', '--output-type', metavar='OUTPUT', default=APIRequestData.CSV_OUTPUT,
                        choices=[APIRequestData.CSV_OUTPUT, APIRequestData.JSON_OUTPUT], help='the output values')

    return parser.parse_args()


def main():
    args = parse_args()
    current_key = 'name'

    def get_key(query_type, key):
        if key != current_key:
            return key
        return query_type[:-1]

    # change to find a specific
    data = {'area': ['se', 'chi', 'ai'],
            'conference': ['SANER', 'INTERACT', 'GECCO'],
            'department': ['UFMG', 'UNICAMP', 'UFPE'],
            'year': [2015, 2016, 2017],
            'researchers': ['Adenilso Simao', 'Julio Dos Reis', 'Rafael Bordini']}

    queries = [
        ('Número de publicações em uma determinada conferência de uma área', 'conferences', ['area', current_key]),
        ('Número de publicações no conjunto de conferências de uma área', 'areas', [current_key]),
        ('Scores de todos os departamentos em uma área', 'departments', ['area']),
        ('Score de um determinado departamento em uma área.', 'departments', ['area', current_key]),
        ('Número de professores que publicam em uma determinada área (organizados por departamentos)',
         'departments',
         ['area']),
        ('Número de professores de um determinado departamento que publicam em uma área',
         'departments',
         ['area', current_key]),
        ('Todos os papers de uma área (ano, título, deptos e autores)', 'papers', ['area']),
        ('Todos os papers de uma área em um determinado ano', 'papers', ['area', 'year']),
        ('Todos os papers de um departamento em uma área', 'papers', ['area', 'department']),
        ('Todos os papers de um professor (dado o seu nome)', 'papers', ['researchers'])
    ]
    num_queries = 1

    for query, data_type, parameters in queries:
        data_map = {key: data[get_key(data_type, key)] for key in parameters}
        print(query)
        for i in range(num_queries):
            query_parameters = {key: data_map[key][i] for key in parameters}
            APIRequestData(args.ip, args.port, data_type, args.output_type, query_parameters).print_output()
            print()
        print('\n\n')
