import argparse
from src.falcon import Falcon
from src.falcon import BANNER
import sys

def main():
    for i in sys.argv:
        if i == "-h" or i == "--help":
            print(BANNER)

    parser = argparse.ArgumentParser(description="none")
    parser.add_argument("-t", "--template", action="store")
    parser.add_argument("-l", "--logic", action="store")
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("-e", "--err", action="store_true")
    parser.add_argument("-o", "--output", action="store")
    parser.add_argument("-c", "--config-file", action="store")
    parser.add_argument("-s", "--show_email", action="store_true")
    parser.add_argument("-S", "--send_email", action="store_true")
    parser.add_argument("-n", "--customer_name", action="store")

    args = parser.parse_args()
    taco = Falcon(args)

    if args.template != None or args.logic != None:
        taco.parse_input()
    else:
        print("Error: a template file must provided to generate an email")
        return


if __name__ == "__main__":
    main()