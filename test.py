import requests
import os
import json

def run_tests():
    url = 'http://localhost:8080/api/score'


    # the tests are the files in test_data, load them into a list
    tests = []
    for test_file in os.listdir('test_data'):
        with open(f'test_data/{test_file}') as file:
            tests.append(json.load(file))

    for test in tests:
        response = requests.post(url, json={'data': test})    
        print(response.json())

    
if __name__ == '__main__':
    run_tests()