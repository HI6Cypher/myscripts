#!/usr/bin/python3
import os
import sys
import time
import json
sys.path.append("../")
from HI6ToolKit.hi6toolkit import HTTP_Request as hp

__doc__ = """
    this script changes file with format (yearmonthday_time.jpg like 20200213_150216.jpg) to solar type
    with this API :
        api.ineo-team.ir/DateConvert.php?method=miladi&day={day}&month={month}&year={year}
        note : this api has request limit, in every 10 second requests must not be more than 7 times"""
dates = list()

def get_url(day : int, month : int, year : int) -> tuple[str, str] :
    host = "api.ineo-team.ir"
    end = f"/DateConvert.php?method=miladi&day={day}&month={month}&year={year}"
    return host, end

def request(host, end) -> bytes:
    r = hp(host, 443, "GET", None, end, True)
    r.request()
    return r.response_header, r.response

def parse_miladi_date(date : str) -> str :
    form = "422"
    p = 0
    result = list()
    for i in form :
        val = date[p:int(i) + p]
        result.append(val)
        p += int(i)
    else : result.append(date[8:])
    return {
            "year" : result[0],
            "month" : result[1],
            "day" : result[2],
            "tail" : result[3]
            }

def get_file_name(path : str) -> "get_file_name iteration" :
    filenames = os.listdir(path)
    for filename in filenames :
        if (
            len(filename) == 19 and
            filename.endswith(".jpg")
            ) : yield filename

def change_name(old_name : str, p : dict) -> None :
    new_name = p["year"] + p["month"] + p["day"] + p["tail"]
    os.rename(old_name, new_name)
    return None

def is_ok_resp(meta : str) -> bool :
    resp = json.loads(meta)
    return True if resp["ok"] else False

def get_new_date_from_json(meta : str) -> dict :
    resp = json.loads(meta)
    new_date = (resp["result"]["convert"]["solar"]["date"]).split("/")
    new_date = {
        "year" : new_date[0],
        "month" : new_date[1],
        "day" : new_date[2]
        }
    return new_date

def save_faileds(name : str) :
    path = "faileds.txt"
    if os.path.exists(path) :
        mode = "a"
    else :
        s = "# this file created for specify failed files in renaming\n\n"
        mode = "w"
    with open(path, mode) as f :
        f.write(f"{name}\n")

def main() -> None :
    path = "./"
    agree = input(f"press ENTER to continue...")
    if agree in ("N", "n") : sys.exit()
    print("[+] starting...")
    names = get_file_name(path)
    for name in names :
        parsed_name = parse_miladi_date(name)
        host, end = get_url(
            parsed_name["day"],
            parsed_name["month"],
            parsed_name["year"]
            )
        print(f"[+] changing {name}", end = " ", flush = True)
        header, meta = request(host, end)
        if is_ok_resp(meta) :
            new_date = get_new_date_from_json(meta)
            new_date["tail"] = parsed_name["tail"]
            change_name(name, new_date)
            print("DONE")
        else :
            print("FAIL")
            save_faileds(name)
        time.sleep(1.5)

main()
