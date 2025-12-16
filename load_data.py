import xml.etree.ElementTree as ET
import requests
import os
import time
import json
import decimal


class load_data:
    def __init__(self):
        self.currencies = {}
        self.timestamp = None
        self.last_updated = None
        self.fetched = None
    def load(self):
        url = "https://www.bnr.ro/nbrfxrates.xml"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            with open('data.xml', 'wb') as f:
                f.write(response.content)
            self.timestamp = time.ctime()
            print(f"Fetch Successful! {self.timestamp}")
            self.fetched = True
            return True
        except requests.RequestException:
            if os.path.exists('cache.json'):
                with open('cache.json', 'r') as f:
                    data = json.load(f)
                    self.currencies = data['currencies']
                    self.timestamp = data['last_updated']
                    self.fetched = False
                print("Uploading from cache.json")
                return False
            elif not os.path.exists('cache.json'):
                print("No cache found!")
                return None
        finally:
            return self.currencies

    def normalize_currencies(self, currencies):
        if currencies is None:
            currencies = self.currencies
        normalized = {'RON' : 1.0000}
        for item in currencies:
            normalized[item['currency']] = round(float(item['Rate']) * float(item['multiplier']),4)
        return normalized


    def parse(self, xml_file='data.xml'):
        if self.fetched == True:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            currencies = []
            cube = root.find('.//{http://www.bnr.ro/xsd}Cube')
            for item in cube.findall('{http://www.bnr.ro/xsd}Rate'):
                currency_data = {
                    'currency': item.attrib['currency'],
                    'Rate': item.text,
                    'multiplier': item.get('multiplier', 1)
                }
                currencies.append(currency_data)
            normalized = self.normalize_currencies(currencies)
            self.currencies = normalized
            self.save_to_json(self.currencies)
            try:
                os.remove(xml_file)
            except OSError:
                print("Error: Could not delete file")
            return self.currencies
        else:
            return self.currencies
    def save_to_json(self, currencies, json_file="cache.json"):
        data = {
            'last_updated': self.timestamp,
            'currencies': currencies
        }
        with open(json_file, 'w') as outfile:
            json.dump(data, outfile)

