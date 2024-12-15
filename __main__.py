import argparse
from src.falcon import Falcon
from src.falcon import BANNER
import sys

def main():
    for i in sys.argv:
        if i == "-h" or i == "--help":
            print(BANNER)

    parser = argparse.ArgumentParser(description="none")
    parser.add_argument(
        "-t", "--template", 
        action="store", 
        help="The text and the variable you want to replace on the email."
    )
    
    parser.add_argument(
        "-l", 
        "--logic", 
        action="store", 
        help="The logic script controls how the email flows."
    )
    
    parser.add_argument(
        "-d", 
        "--debug", 
        action="store_true", 
        help="Displays debug messages."
    )
    
    parser.add_argument(
        "-e", 
        "--err", 
        action="store_true", 
        help="Disables error messages."
    )
    
    parser.add_argument(
        "-o", 
        "--output", 
        action="store", 
        help="Write the output to a file."
    )
    
    parser.add_argument(
        "-c", 
        "--config-file", 
        action="store", 
        help="Configures prefilling of email fields like from, to, cc, etc."
    )
    
    parser.add_argument(
        "-s", 
        "--show_email", 
        action="store_true", 
        help="Displays the email is a new windows - (Outlook only)."
    )
    
    parser.add_argument(
        "-S", 
        "--send_email", 
        action="store_true", 
        help="Sends the email without writing to a file or displaying it (Outlook Only)."
    )

    parser.add_argument(
        "-n", 
        "--customer_name", 
        action="store", 
        help="Only send emails to select few email addresses (Experimental)."
    )

    args = parser.parse_args()
    taco = Falcon(args)

    if args.template != None or args.logic != None:
        taco.parse_input()
    else:
        print("Error: a template file must provided to generate an email")
        return


if __name__ == "__main__":
    main()