import requests
import os
import json

def run_tests():
    url = 'http://localhost:8080/api/score'


    # the tests are the files in test_data, load them into a list
    tests = []
    for test_file in os.listdir('test_data'):
        if test_file.endswith('.json'):            
            with open(f'test_data/{test_file}') as file:
                test_data = json.load(file)
                response = requests.post(url, json={'data': test_data})    
                print(test_file, response.json())
                print('\n\n\n')

    
if __name__ == '__main__':
    run_tests()