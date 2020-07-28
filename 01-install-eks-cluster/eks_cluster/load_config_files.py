import json

def read_helm_config(filename):
    with open(filename, 'r') as stream:
        return stream.read()