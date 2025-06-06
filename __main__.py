"""Run chess.py in src folder"""



def loading() -> None:
    list_logout = ["\\", "|", "/", "-"]
    for i in range(3):
        for j in list_logout:
            print("\rQuiting in {} seconds {}".format(3 - i, j), end = "")
            sleep(0.25)



try:
    from sys import version_info
    from time import sleep
    from src.chess import main
except:
    print("Import error")
    loading()
    quit()



if __name__ == '__main__':
    major_version, minor_version, *_ = version_info
    if major_version < 3 or minor_version < 7:
        print("Your Python version is lower than Python 3.7")
        loading()
        quit()
    main()