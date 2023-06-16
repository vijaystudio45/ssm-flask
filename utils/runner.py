from multiprocessing import Process
from mailer import _driver

def f(name):
    print("hello", name)

if __name__ == "__main__":
    p = Process(target=_driver)
    p.start()
    p.join()
