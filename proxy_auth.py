from mitmproxy import http
import base64

proxy_user = "STm87nUFS6"
proxy_pass = "6StepJYs2y"

credentials = f"{proxy_user}:{proxy_pass}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()

def http_connect(flow: http.HTTPFlow):
    flow.request.headers["Proxy-Authorization"] = f"Basic {encoded_credentials}"

def request(flow: http.HTTPFlow):
    flow.request.headers["Proxy-Authorization"] = f"Basic {encoded_credentials}"