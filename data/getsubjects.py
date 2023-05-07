import requests
import json
import csv
import random
import time

data = []
i = 0
with open("./library_management_api_books.csv", 'r') as file:
  csvreader = csv.reader(file)
  for row in csvreader:
    if (row[5] != 'isbn13' and i in range(9000,11123)):
      response_API = requests.get('https://openlibrary.org/search.json?isbn='+row[5])
      parse_json = json.loads(response_API.text)
      try:
        if 'subject' in parse_json['docs'][0]:
          row.append([i for i in random.choices(parse_json['docs'][0]['subject'],k=int(len(parse_json['docs'][0]['subject'])/2)) if i.isalpha()])
        #   row.append(parse_json['docs'][0]['subject'])
      except:
        print(parse_json['numFound'], row[5], i)
      row[0] = i+1
      data.append(row)      
    i = i + 1
    if (i == 11123):
      break
    if (i%500 == 0):
      time.sleep(20)

with open('./books5.csv', 'w') as file:
  writer = csv.writer(file)
  for row in data:
    writer.writerow(row)