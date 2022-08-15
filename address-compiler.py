def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)



install_and_import('requests')
install_and_import('bs4')
install_and_import('pandas')

import urllib.parse
import json
from bs4 import BeautifulSoup
import pandas as pd
from functools import reduce

session = requests.Session()

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

params = {
    'interviewID': 'PublicSearch',
    'workspace': 'main',
    'lang': 'en',
}

cookie_response = session.get('https://gpas.guelph.ca/smartlets/do.aspx', params=params, headers=headers)

address_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # Requests sorts cookies= alphabetically
    # 'Cookie': 'ASP.NET_SessionId=pkmx0p4nqm0akp4kkfwyopb2; locale_pref=en',
    'DNT': '1',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

def getParams(address):
    return {
        't_address_search': '1',
        'term': address,
        '_type': 'query',
        'q': address,
    }

with open("input.txt", "r") as f:
    lines = f.readlines()
    addresses = [line.rstrip() for line in lines]

dfs = []
for address in addresses:
    try:
        print(address)

        address_fetch_successful = False

        address_to_try = address

        valid_addresses = []
        while " " in address_to_try and not address_fetch_successful:
            print("Trying " + address_to_try)
            try:
                address_encoded = urllib.parse.quote_plus(address)
                correct_address_response = session.get('https://gpas.guelph.ca/smartlets/do.aspx', params=getParams(address_to_try), headers=address_headers)

                for address_json in correct_address_response.json():
                    address_string = "{};{};{};{};{};;".format(
                            address_json['house'],
                            address_json['city'],
                            address_json['name'],
                            address_json['type'],
                            address_json['direction'])
                    valid_addresses.append(address_string)
                    address_fetch_successful = True

                if not address_fetch_successful:
                    print("Failed with " + address_to_try)
                    address_to_try = address_to_try.rsplit(' ', 1)[0].strip()
            except:
                print("Excepted     Failed with " + address_to_try)
                address_to_try = address_to_try.rsplit(' ', 1)[0].strip()

        for address in valid_addresses:
            headers = {
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryBUhDUfYG0xB5d62G',
                # Requests sorts cookies= alphabetically
                # 'Cookie': 'locale_pref=en; com.alphinat.sgs.anticsrftoken=yLlII9PEDjez8DoeR%2B9jzC49YUfpr%2FXJ2SGiLb8DtwPt1DrYQcD3j7qDyfTVBv48cZ%2FNEPC5r43VcQyiDoTz9g%3D%3D; ASP.NET_SessionId=mignchwwa0aqxktdnh3bslgt',
                'DNT': '1',
                'Origin': 'https://gpas.guelph.ca',
                'Pragma': 'no-cache',
                'Referer': 'https://gpas.guelph.ca/smartlets/do.aspx?interviewID=PublicSearch&workspace=main&lang=en',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest',
                'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
            }

            data = '------WebKitFormBoundaryBUhDUfYG0xB5d62G\r\nContent-Disposition: form-data; name="com.alphinat.sgs.anticsrftoken"\r\n\r\n\r\n------WebKitFormBoundaryBUhDUfYG0xB5d62G\r\nContent-Disposition: form-data; name="d_1607626896958"\r\n\r\nhttps://gpas.guelph.ca/CPFAPublicSearch/rest\r\n------WebKitFormBoundaryBUhDUfYG0xB5d62G\r\nContent-Disposition: form-data; name="d_1628281973985"\r\n\r\n1,1000\r\n------WebKitFormBoundaryBUhDUfYG0xB5d62G\r\nContent-Disposition: form-data; name="d_1628018157419"\r\n\r\n1,4,7,8,9,10,11,14,19,21,25,26,29,31,32,34,40,41,43,44,50,51,59,61,62,65,67,68,70,75,1002,1006,1032,1033,1034\r\n------WebKitFormBoundaryBUhDUfYG0xB5d62G\r\nContent-Disposition: form-data; name="d_1629387420475"\r\n\r\n{}\r\n------WebKitFormBoundaryBUhDUfYG0xB5d62G\r\nContent-Disposition: form-data; name="e_1501060574930"\r\n\r\nonclick\r\n------WebKitFormBoundaryBUhDUfYG0xB5d62G\r\nContent-Disposition: form-data; name="isAjax"\r\n\r\ntrue\r\n------WebKitFormBoundaryBUhDUfYG0xB5d62G--\r\n'.format(address_string)


            response = session.post('https://gpas.guelph.ca/smartlets/do.aspx', headers=headers, data=data)

            # print("ICI" in response.text)

            soup = BeautifulSoup(response.text, 'html.parser')
            header = soup.find_all("table")[0].find("tr")

            list_header = []
            data = []
            for items in header:
                try:
                    list_header.append(items.get_text())
                except:
                    continue

            # for getting the data
            HTML_data = soup.find_all("table")[0].find_all("tr")[1:]

            for element in HTML_data:
                sub_data = []
                for sub_element in element:
                    try:
                        sub_data.append(sub_element.get_text())
                    except:
                        continue
                data.append(sub_data)

            header = [i for i in list_header if i != '\n']
            #print(header)

            rows = []
            for i in data:
                row = []
                for j in i:
                    if j != '\n':
                        formattedString = j.replace("\t", "").replace("\r", "").replace("\n", "").strip()
                        row.append(formattedString)
                rows.append(row)

            #print(rows)

            df = pd.DataFrame(columns=header, data=rows)
            dfs.append(df)
            print("Address " + address + " Successful")
    except Exception as e:
        print("Address Failed " + address + " Reason: " +  e)

# for df in dfs:
#    print(df.columns)

data_merge = pd.concat(dfs)
#print(data_merge)                           # Print merged DataFrame
#print(data_merge.head())
data_merge.to_csv("output.csv")

