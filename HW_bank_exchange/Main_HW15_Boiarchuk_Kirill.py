import requests
import pandas as pd
import xml.etree.ElementTree as et
import datetime
from requests.exceptions import HTTPError

# Адрес api метода для запроса get
url = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange'

# current_datetime = datetime.date.today()
# print(current_datetime)
# Отправляем get request (запрос GET)
try:
    response = requests.get(url)
    response.raise_for_status()
except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
except Exception as err:
    print(f'Other error occurred: {err}')
finally:
    current_datetime = datetime.date.today()
    print(current_datetime)
    tree = et.ElementTree(et.fromstring(response.text))
    root = tree.getroot()
    df_cols = ["charcode", "name", "for", "value"]
    rows = []
    for node in root:
        s_charcode = node.find("cc").text if node is not None else None
        s_name = node.find("txt").text if node is not None else None
        s_value = node.find("rate").text if node is not None else None

        rows.append({"charcode": s_charcode, "name": s_name, "for": "to UAH:", "value": s_value})

    result = pd.DataFrame(rows, columns=df_cols)
    result.index += 1
    with pd.option_context("display.max_rows", None, "display.max_columns", None):
        print(result)

tfile = open('test.txt', 'a')
tfile.write(result.to_string())
tfile.close()

