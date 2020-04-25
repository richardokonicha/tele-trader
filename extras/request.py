
headers = {'hmac': "4ec11f47ed22830713fb4a7c1fcbec28171f215ef1c7e6298f7cd90d9ecbfcf7bd41ce168d566265be15a3251ff8bd79f215a56dee115a216235953c8c248430"}

encoded = b'amount=0.9&currency1=BTC&currency2=BTC&ipn_url=https%3A%2F%2F42d4741e.ngrok.io%2Fpay&cmd=create_transaction&key=953b0c668c9d75c2d3da984f62a00fd269dc66c6da701250a0d7e14b52449183&version=1&format=json'

sig = '4ec11f47ed22830713fb4a7c1fcbec28171f215ef1c7e6298f7cd90d9ecbfcf7bd41ce168d566265be15a3251ff8bd79f215a56dee115a216235953c8c248430'

url = 'https://www.coinpayments.net/api.php'

params = {'amount': Decimal('0.9'), 'cmd': 'create_transaction', 'currency1': 'BTC', 'currency2': 'BTC', 'format': 'json', 'ipn_url': 'https://42d4741e.ng...ok.io/pay', 'key': '953b0c668c9d75c2d3d...b52449183', 'version': 1}

request_method = "post"




headers['Content-Type'] = 'application/x-www-form-urlencoded'

def request(self, request_method, **params):
    """
    The basic request that all API calls use
    the parameters are joined in the actual api methods so the parameter
    strings can be passed and merged inside those methods instead of the
    request method
    """
    encoded, sig = self.create_hmac(**params)

    headers = {'hmac': sig}

    if request_method == 'get':
        req = urllib.request.Request(self.url, headers=headers)
    elif request_method == 'post':
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        req = urllib.request.Request(self.url, data=encoded, headers=headers)
    try:
        # proxy_support = urllib.request.ProxyHandler(
        #     {"http" : "http://ahad-haam:3128"}
        #     )
        # opener = urllib.request.build_opener(proxy_support)


        # proxy  = urllib2.ProxyHandler({'http': os.environ.get('FIXIE_URL', '')})
        proxy  = urllib.ProxyHandler({'http': "http://fixie:cIOCBSpAPnau6FY@olympic.usefixie.com:80"})

        auth   = urllib.HTTPBasicAuthHandler()
        opener = urllib.build_opener(proxy, auth, urllib.HTTPHandler)
        urllib.request.install_opener(opener)

        # response = opener.open('http://www.example.com')


        response = urllib.request.urlopen(req)
        status_code = response.getcode()
        response_body = response.read()
    except urllib.error.HTTPError as e:
        status_code = e.getcode()
        response_body = e.read()
    return json.loads(response_body)




# b'{"error":"This API key may not be used from this IP address: 129.205.113.163","result":[]}'



#  def request(self, request_method, **params):
#         """
#         The basic request that all API calls use
#         the parameters are joined in the actual api methods so the parameter
#         strings can be passed and merged inside those methods instead of the
#         request method
#         """
#         encoded, sig = self.create_hmac(**params)

#         headers = {'hmac': sig}

#         if request_method == 'get':
#             req = urllib.request.Request(self.url, headers=headers)
#         elif request_method == 'post':
#             headers['Content-Type'] = 'application/x-www-form-urlencoded'
#             req = urllib.request.Request(self.url, data=encoded, headers=headers)
#         try:
#             response = urllib.request.urlopen(req)
#             status_code = response.getcode()
#             response_body = response.read()
#         except urllib.error.HTTPError as e:
#             status_code = e.getcode()
#             response_body = e.read()
#         return json.loads(response_body)

# export http_proxy='http://myproxy.example.com:1234'

# req.set_proxy(proxy_host, 'http')




# import urllib.request as request

# # disable proxy by passing an empty
# proxy_handler = request.ProxyHandler({})
# # alertnatively you could set a proxy for http with
# # proxy_handler = request.ProxyHandler({'http': 'http://fixie:cIOCBSpAPnau6FY@olympic.usefixie.com:80'})

# opener = request.build_opener(proxy_handler)

# url = 'http://www.example.org'

# # open the website with the opener
# req = opener.open(url)
# data = req.read().decode('utf8')
# print(data)


import os, requests
proxyDict = { 
              "http"  : os.environ.get('FIXIE_URL', ''), 
              "https" : os.environ.get('FIXIE_URL', '')
            }
r = requests.get('http://www.example.com', proxies=proxyDict)


r = requests.post(url, data=encoded,  headers=headers, proxies=proxyDict)
