
import requests,datetime

greet=str(datetime.datetime.now())
r=requests.get('http://localhost:5000/api/pallot/'+greet)
