#!/usr/bin/python3
from khayyam import JalaliDate
import datetime
import os
import sys
import time

def convert(year : int, month : int, day : int) -> str :
    date = JalaliDate(datetime.date(year, month, day))
    result = str(date).replace("-", "")
    return result

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
            "year" : int(result[0]),
            "month" : int(result[1]),
            "day" : int(result[2]),
            "tail" : result[3]
            }

def get_file_name(path : str, file_format : str) -> str :
    filenames = os.listdir(path)
    for filename in filenames :
        if (
            len(filename) == (16 + len(file_format)) and
            filename.endswith(file_format)
            ) :
            yield filename

def change_name(old_name : str, new_name : dict) -> None :
    os.rename(old_name, new_name)
    return

def main() -> None :
    path = input("enter path(type ./ for current dir) : ")
    file_format = input("enter file format without dot(like xyz not .xyz) : ")
    agree = input(f"are u agree to start renaming pictures of {path} dir? [Y/n] : ")
    if agree == "N" : sys.exit()
    print("[+] starting...")
    names = get_file_name(path, file_format)
    for name in names :
        parsed_name = parse_miladi_date(name)
        new_date = convert(
            parsed_name["year"],
            parsed_name["month"],
            parsed_name["day"]
            )
        new_date = new_date + parsed_name["tail"]
        print(f"[+] changing {name}", end = " ", flush = True)
        change_name(name, new_date)
        print("DONE")
main()
