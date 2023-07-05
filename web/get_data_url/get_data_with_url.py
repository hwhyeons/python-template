from urllib.request import urlopen
from urllib.parse import quote

url = 'http://localhost:8080/getAllWorkByDate?date=2023-07-03'
# 실행하고자 하는 url에 한글이 포함되어있는 경우, quote("내용") 이렇게 보내면 됨
f = urlopen(url)
myfile = f.read()
print(myfile)
