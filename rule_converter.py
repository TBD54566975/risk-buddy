import csv
import json
import sys


def json_to_csv(json_file, csv_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    rules = data.get('rules', [])

    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Condition', 'Action', 'Message'])
        for rule in rules:
            writer.writerow([rule['condition'], rule['action'], rule['message']])


def csv_to_json(csv_file, json_file):
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        rules = [row for row in reader]

    data = {'rules': rules}

    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python rule_converter.py <json_to_csv|csv_to_json> <input_file> <output_file>")
        sys.exit(1)

    operation, input_file, output_file = sys.argv[1], sys.argv[2], sys.argv[3]

    if operation == 'json_to_csv':
        json_to_csv(input_file, output_file)
    elif operation == 'csv_to_json':
        csv_to_json(input_file, output_file)
    else:
        print("Unknown operation")
        sys.exit(1)
