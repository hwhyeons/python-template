from urllib.request import urlopen

url = 'http://localhost:8080/getAllWorkByDate?date=2023-07-03'
f = urlopen(url)
myfile = f.read()
print(myfile)
