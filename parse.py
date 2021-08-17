import requests
from bs4 import BeautifulSoup
import json
import os
import re

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
#subjects_id = [1,2,3,4,5,6,7,8,9,10,11,12,13,18,22]
subjects_id = [7]
with open('subjects.json') as f:
    subjects = json.load(f)
for i in subjects_id:
    data =f'''"subjectId":{i},
        "levelIds":[],
        "themeIds":[],
        "typeIds":[],
        "id":"",
        "favorites":0,
        "answerStatus":0,
        "themeSectionIds":[],
        "published":0,
        "extId":"",
        "fipiCode":"",
        "docId":"",
        "isAdmin":true,
        "loadDates":[],
        "isPublished":false,
        "pageSize":5,
        "pageNumber":1'''

    response = requests.post('http://os.fipi.ru/api/tasks', headers=headers, cookies=cookies, data="{"+data+"}", verify=False)
    jss = response.json()
    tasks = jss['tasks']
    if subjects[str(i)] not in os.listdir():
        os.mkdir(f"{subjects[str(i)]}")
    os.chdir(f"{subjects[str(i)]}")
    for task in tasks:
        if task['taskTypeId'] == 1:
            text = " ".join(list(map(lambda x: x.text, BeautifulSoup(task['taskTextWord'],'lxml').findAll("p"))))
            text = re.sub('\\r\\n\\\\*', ' ', text)
            data = {
                "id": task["id"],
                "taskTypeId": task["taskTypeId"],
                "answer": task["answer"],
                "text": text,
            }
        elif task['taskTypeId'] == 2:
            parsed_html = BeautifulSoup(task['html'],'lxml')
            answers = list(map(lambda x: x.text.strip(), parsed_html.findAll("div",{"class":"answer"})))
            text = " ".join(list(map(lambda x: x.text, BeautifulSoup(task['taskTextWord'],'lxml').findAll("p"))))
            text = re.sub('\\r\\n\\\\*', ' ', text)
            data = {
                "id": task["id"],
                "taskTypeId": task["taskTypeId"],
                "answer_index": int(task['answer'])-1,
                "answers": answers,
                "text": text,
            }
            themeNameId = task['themeNames'][0].split()[0]
            if f"{themeNameId}.json" not in os.listdir():
                with open(f'{themeNameId}.json', 'w') as f:
                    json.dump([data], f, ensure_ascii=False, indent=2)
            else:
                with open(f'{themeNameId}.json') as f:
                    old_data = json.load(f)
                old_data += [data]
                with open(f'{themeNameId}.json', 'w') as f:
                    json.dump(old_data, f, ensure_ascii=False, indent=2)
