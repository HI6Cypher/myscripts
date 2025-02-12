#!/usr/bin/python3
import subprocess as sp
import re
import sys
import os

DIR = "ffmpeg_output"
ffmpeg_command = lambda x, y : f"ffmpeg -hwaccel cuda -i .\{x} -c:v libx264 -c:a copy .\{DIR}\{y}".split()

def prepare_inputs() -> list[str] :
    return os.listdir()

def filter(x : list, pat : str) -> list :
    regex = re.compile(pat)
    filtered = set()
    for i in x :
        if re.search(regex, i) : filtered.add(i)
    else : return filtered

def make_output_dir() -> None :
    if not os.path.exists(DIR) : os.mkdir(DIR)
    return None

def convert_name(file : str) :
    return file.removesuffix("_.mp4") + ".mp4"

def convert(file : str) -> bool :
    print("fd")
    old_name = file
    new_name = convert_name(file)
    command = ffmpeg_command(old_name, new_name)
    output = sp.run(command)
    return True if output.returncode == 0 else False

def main() -> None :
    make_output_dir()
    files = prepare_inputs()
    pattern = r"\d{8}_\d{6}_.mp4"
    files = filter(files, pattern)
    for file in files :
        status = convert(file)
        if status == False :
            if input("conversion wasn't successful, 'q' : exit, 'y' : continue\n>>> ") == "q" : sys.exit()
        else : print("\n")
    else : print("outputs stored in 'ffmpeg_output' directory")

main()


