import os
while True :
    try :
        i = input("$HI6_COMMAND>>>")
    except KeyboardInterrupt :
        exit(0)
    except :
        exit(1)
    else :
        text = f"@ echo off\npython.exe hi6toolkit.py {i}\npause"
        if i not in ["clear", "cls"] :
            with open("hi6toolkit.bat", "w") as file :
                file.write(text)
            os.system("hi6toolkit.bat")
        else :
            os.system("cls || clear")        