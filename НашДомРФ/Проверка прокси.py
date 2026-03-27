import requests

proxy = "http://mix332CS48TLI:wj0bJrzE@213.232.121.244:8080"

proxies = {
    "http": proxy,
    "https": proxy
}

r = requests.get(
    "https://api.ipify.org?format=json",
    proxies=proxies,
    timeout=10
)

print(r.status_code)
print(r.text)