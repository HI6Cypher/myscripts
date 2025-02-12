#!/usr/bin/python3
from HI6ToolKit.hi6toolkit import HTTP_Request as hp
import asyncio
import re, time, sys

tasks = list()
urls = list()
pattern = re.compile(r"(?<=server: ).*(?=\r\n)")
success = dict()
failure = list()

async def head_request(host : str, port : int) :
    ssl = True if port == 443 else False
    http = hp(host, port, "HEAD", None, "/", ssl)
    try :
        http.request()
    except Exception as error :
        print("\n\n" + "ERROR : " + error + "\n\n")
        return 0
    else :
        if http.response_header :
            header = http.response_header
            return header
        else :
            return 0

async def isweak(header : bytes) :
    global pattern
    weaks = ("apache", "nginx", "litespeed", "lighttpd", "caddy")
    if "server" in header :
        server = re.search(pattern, header)
        if server :
            server = server.group().strip()
            if server.lower() in weaks : return (True, server)
            else : return (False, server)
        else : return (True, "Unknown")

async def parse_url(url : str) :
    if url.startswith("https://") :
        host = url[8:]
        port = 443
        return (host, port)
    elif url.startswith("http://") :
        host = url[7:]
        port = 80
        return (host, port)
    else :
        return (url, 80)

async def scan(url : str) :
    global success, failure
    host, port = await parse_url(url)
    header = await asyncio.create_task(head_request(host, port))
    if header :
        print(f"[*] is server {host}:{port} weak?", end = "  ")
        weak, server = await isweak(header.lower())
        if weak :
            print(f"server : {server}  \033[32mYES\033[0m")
            success[url] = server
        else : print(f"server : {server}  \033[31mNO\033[0m")
    else : failure.append(url)
    return None

async def main() :
    global urls, tasks
    for url in urls[::-1] :
        tasks.append(asyncio.create_task(scan(url)))
        urls.pop()
    else :
        await asyncio.gather(*tasks, return_exceptions = True)
    return None

if __name__ == "__main__" :
    try :
        t = time.time()
        if len(sys.argv) <= 1 : raise Exception("enter arg")
        path = sys.argv[1]
        print(f"[+] opening file {path}", end = "  ")
        with open(path, "r") as file :
            index = file.read().split("\n")
        print("\033[32mDONE\033[0m")
        urls = index
        print("[+] SCANING servers...")
        asyncio.run(main())
    except Exception as error : print(error or "ERROR")
    except KeyboardInterrupt : print("CTRL C  exiting...")
    else :
        print("[+] writing in weaks.txt", end = "  ")
        with open("weaks.txt", "w") as file :
            for url, server in success.items() :
                file.write(f"{url} -> {server}\n")
            else : print("\033[32mDONE\033[0m")
        print(f"\nDONE in \033[93m{round(time.time() - t, 2)}\033[0m")
