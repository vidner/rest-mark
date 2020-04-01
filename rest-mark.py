#! /usr/bin/python3
import click
import requests
import json
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import time
from tqdm import tqdm

def summary(time_taken,total_request,result):
    http_status_dict = {"100" : "Continue", "101" : "Switching Protocols", "102" : "Processing", "200" : "OK", "201" : "Created", "202" : "Accepted", "203" : "Non-authoritative Information", "204" : "No Content", "205" : "Reset Content", "206" : "Partial Content", "207" : "Multi-Status", "208" : "Already Reported", "226" : "IM Used", "300" : "Multiple Choices", "301" : "Moved Permanently", "302" : "Found", "303" : "See Other", "304" : "Not Modified", "305" : "Use Proxy", "307" : "Temporary Redirect", "308" : "Permanent Redirect", "400" : "Bad Request", "401" : "Unauthorized", "402" : "Payment Required", "403" : "Forbidden", "404" : "Not Found", "405" : "Method Not Allowed", "406" : "Not Acceptable", "407" : "Proxy Authentication Required", "408" : "Request Timeout", "409" : "Conflict", "410" : "Gone", "411" : "Length Required", "412" : "Precondition Failed", "413" : "Payload Too Large", "414" : "Request-URI Too Long", "415" : "Unsupported Media Type", "416" : "Requested Range Not Satisfiable", "417" : "Expectation Failed", "418" : "I'm a teapot", "421" : "Misdirected Request", "422" : "Unprocessable Entity", "423" : "Locked", "424" : "Failed Dependency", "426" : "Upgrade Required", "428" : "Precondition Required", "429" : "Too Many Requests", "431" : "Request Header Fields Too Large", "444" : "Connection Closed Without Response", "451" : "Unavailable For Legal Reasons", "499" : "Client Closed Request", "500" : "Internal Server Error", "501" : "Not Implemented", "502" : "Bad Gateway", "503" : "Service Unavailable", "504" : "Gateway Timeout", "505" : "HTTP Version Not Supported", "506" : "Variant Also Negotiates", "507" : "Insufficient Storage", "508" : "Loop Detected", "510" : "Not Extended", "511" : "Network Authentication Required", "599" : "Network Connect Timeout Error"}
    print("Benchmark finished with",total_request,"Request in",time_taken,"second")
    for i,j in result.items():
        print(j,"Request with status [%s]" % str(i), http_status_dict[str(i)])
def get(req):
    url = req[0]
    headers = json.loads(req[1])
    resp = requests.get(url, headers=headers,stream=True)
    return resp.status_code

def delete(req):
    url = req[0]
    headers = json.loads(req[1])
    resp = requests.delete(url, headers=headers,stream=True)
    return resp.status_code
    
def post(req):
    url = req[0]
    headers = json.loads(req[1])
    data = json.loads(req[2])
    resp = requests.post(url, json=data, headers=headers)
    return resp.status_code

def put(req):
    url = req[0]
    headers = json.loads(req[1])
    data = json.loads(req[2])
    resp = requests.put(url, json=data, headers=headers)
    return resp.status_code

@click.command()
@click.option('-n','--count', default=1, help='number of request')
@click.option('-u','--url', required=True, type=str,help='api url')
@click.option('-s','--single', is_flag=True, help='single thread, by default is multi-thread')
@click.option('-w','--worker', default=10, help='default worker is 10')
@click.option('-d','--data', default="{ }", help='in json format')
@click.option('-h','--headers', default="{ }", help='in json format')
@click.argument('method')
def rest_mark(count, method, url, single, worker, data, headers):
    """
    avaiable methods : get,post,put,delete
    """
    req = [[url,headers,data]]*count
    if method=="get":
        if single:
            out = []
            start = time()
            for i in tqdm(req):
                out.append(get(i))
            time_taken = time()-start
            key = Counter(out).keys()
            val = Counter(out).values()
            res = {k: v for d in range(len(key)) for k, v in zip(key,val)}
            summary(time_taken,count,res)
        else:
            out = []
            start = time()
            with ThreadPoolExecutor(max_workers=worker) as executor:
                processes = list(tqdm(executor.map(get,req), total=count))
            for task in processes:
                out.append(task)
            time_taken = time()-start
            key = Counter(out).keys()
            val = Counter(out).values()
            res = {k: v for d in range(len(key)) for k, v in zip(key,val)}
            summary(time_taken,count,res)
    
    elif method=="delete":
        if single:
            out = []
            start = time()
            for i in tqdm(req):
                out.append(delete(i))
            time_taken = time()-start
            key = Counter(out).keys()
            val = Counter(out).values()
            res = {k: v for d in range(len(key)) for k, v in zip(key,val)}
            summary(time_taken,count,res)
        else:
            out = []
            start = time()
            with ThreadPoolExecutor(max_workers=worker) as executor:
                processes = list(tqdm(executor.map(delete,req), total=count))
            for task in processes:
                out.append(task)
            time_taken = time()-start
            key = Counter(out).keys()
            val = Counter(out).values()
            res = {k: v for d in range(len(key)) for k, v in zip(key,val)}
            summary(time_taken,count,res)

    elif method=="post":
        if single:
            out = []
            start = time()
            for i in tqdm(req):
                out.append(post(i))
            time_taken = time()-start
            key = Counter(out).keys()
            val = Counter(out).values()
            res = {k: v for d in range(len(key)) for k, v in zip(key,val)}
            summary(time_taken,count,res)
        else:
            out = []
            start = time()
            with ThreadPoolExecutor(max_workers=worker) as executor:
                processes = list(tqdm(executor.map(post,req), total=count))
            for task in processes:
                out.append(task)
            time_taken = time()-start
            key = Counter(out).keys()
            val = Counter(out).values()
            res = {k: v for d in range(len(key)) for k, v in zip(key,val)}
            summary(time_taken,count,res)

    elif method=="put":
        if single:
            out = []
            start = time()
            for i in tqdm(req):
                out.append(put(i))
            time_taken = time()-start
            key = Counter(out).keys()
            val = Counter(out).values()
            res = {k: v for d in range(len(key)) for k, v in zip(key,val)}
            summary(time_taken,count,res)
        else:
            out = []
            start = time()
            with ThreadPoolExecutor(max_workers=worker) as executor:
                processes = list(tqdm(executor.map(put,req), total=count))
            for task in processes:
                out.append(task)
            time_taken = time()-start
            key = Counter(out).keys()
            val = Counter(out).values()
            res = {k: v for d in range(len(key)) for k, v in zip(key,val)}
            summary(time_taken,count,res)
    else:
        print("avaiable methods : get,post,put,delete")
if __name__ == '__main__':
    rest_mark()

