import json
import requests
import collections


API_KEY = ''
LANGUAGE = 'fr'
INPUT_FILE = 'en-US.json'


def main():

    parsed_json = parse_json(INPUT_FILE)

    values = get_values(parsed_json)

    translated_values = []

    for chunk in [values[x:x+100] for x in xrange(0, len(values), 100)]:
        
        response = None

        try: response = json.loads(send_request(LANGUAGE, API_KEY, *chunk).text, object_pairs_hook=collections.OrderedDict)
        except: pass

        if response: translated_values.extend(item['translatedText'].replace(' +', '').replace('+ ', '') for item in response['data']['translations'])

    output_txt(json.dumps(create_json(parsed_json, translated_values), indent=4, sort_keys=True))


def create_json(source_json, translated_values):

    result_json = collections.OrderedDict()

    for item in source_json.items():

        if isinstance(item[1], str):
            result_json[item[0]] = translated_values.pop(0)
        else:
            result_json[item[0]] = create_json(item[1], translated_values)
            
    return result_json


def get_values(source_json):

    values = []

    for item in source_json.items():
        values.extend([item[1]] if isinstance(item[1], str) else get_values(item[1]))

    return values


def parse_json(json_file):

    with open(json_file) as source_file:
        return json.load(source_file, object_pairs_hook=collections.OrderedDict)


def output_txt(content):

    with open(LANGUAGE + '.json', 'w') as output_file:
        try: output_file.write(content.encode('utf8'))
        except: pass


def send_request(lang, key, *queries):

    return requests.get('https://www.googleapis.com/language/translate/v2', params={'target': lang, 'key': key, 'q': map(lambda x: x.replace(' ', '+'), queries)})


if __name__ == '__main__':
    main()
