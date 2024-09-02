#!/usr/bin/env python

import sys
import requests

def main():
    if len(sys.argv) !=2:
        print("Use: {} <address>".format(sys.argv[0]))
        sys.exit()

    idx=0
    route = sys.argv[1]
    robots = ""
    r = requests.get("http://{}/robots.txt".format(sys.argv[1]))
    robots = r.text
    route = robots.split('\n')[1].split('/')[1].strip()
    while "{" not in robots:
        r = requests.get("http://{}/{}/robots.txt".format(sys.argv[1],route))
        robots = r.text
        print(idx,robots.split('\n'))
        print(idx,robots.split('\n')[1].split('/')[1])
        route = robots.split('\n')[1].split('/')[1].strip() # ¯\_(ツ)_/¯ im lazy for regex
        print("goto")
        idx+=1

if __name__ == "__main__":
    main()