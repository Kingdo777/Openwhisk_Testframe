import time


def main(dict):
    time.sleep(30)
    if 'name' in dict:
        name = dict['name']
    else:
        name = "stranger"
    greeting = "Hello " + name + "!"
    print(greeting)
    return {"greeting": greeting}
