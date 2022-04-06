from requests import get


print(get('http://127.0.0.1:5000/api/news').json())
print(get('http://localhost:5000/api/news/1').json())
print(get('http://localhost:5000/api/news/999').json())
print(get('http://localhost:5000/api/news/q').json())