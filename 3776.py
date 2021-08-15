# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

cookies = {
    '__ddg1': 'hgJdZO3GDZdVXwJW2opu',
    '__ddg2': 'oXvq7SwnIcZPrg1I',
    'sessionId': 'a5daea75-7f55-43a3-5f0e-b685d3f2a3d7',
}

headers = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'sessionId': 'a5daea75-7f55-43a3-5f0e-b685d3f2a3d7',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'http://os.fipi.ru',
    'Referer': 'http://os.fipi.ru/tasks/5/a',
    'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
}

data = '{"subjectId":"5","levelIds":[],"themeIds":[],"typeIds":[],"id":"","favorites":0,"answerStatus":0,"themeSectionIds":[],"published":0,"extId":"","fipiCode":"","docId":"","isAdmin":false,"loadDates":[],"isPublished":false,"pageSize":5,"pageNumber":1}'

response = requests.post('http://os.fipi.ru/api/tasks', headers=headers, cookies=cookies, data=data, verify=False)
jss = response.json()
rofl = jss['tasks'][0]['html'].strip()
checkBoxNumber = jss['tasks'][1]['answer']
print(checkBoxNumber)
parsed_html = BeautifulSoup(rofl,'lxml')
ann = parsed_html.findAll("div",{"class":"answer","id":f"answer_{checkBoxNumber}"})
print(ann[1])
