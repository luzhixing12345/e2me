import argparse
import os
import shutil
import toml

from send_email import send_email
from receive_email import receive_email

CONFIG_NAME = "e2me.toml"


def test_email(config):
    
    email_addr = config["email"]["email"]
    password = config["email"]["passwd"]
    smtp_server = config["email"]["smtp_server"]
    pop3_server = config["email"]["pop3_server"]
    
    # test send email
    send_email(config)
    
    # test receive email
    receive_email(config)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd", type=str, nargs="*", help="init run test get")
    args = parser.parse_args()

    default_config_path = os.path.join(os.path.dirname(__file__), CONFIG_NAME)

    if len(args.cmd) == 1 and args.cmd[0] == "init":
        if os.path.exists(CONFIG_NAME):
            print(f"Config file already exists: {CONFIG_NAME}")
        else:
            # copy default config file
            shutil.copyfile(default_config_path, CONFIG_NAME)
            print(f"Config file created: {CONFIG_NAME}")
        return

    if not os.path.exists(CONFIG_NAME):
        print(f"Config file not found: {CONFIG_NAME}\n")
        print("Please run 'e2me init' to create a new config file.")
        exit(1)

    if len(args.cmd) == 0:
        # print help info
        parser.print_help()
        exit(0)

    config = toml.load(CONFIG_NAME)

    if args.cmd[0] == "run":
        send_email(config)
    elif args.cmd[0] == "test":
        test_email(config)
    elif args.cmd[0] == "get":
        receive_email(config)
    else:
        print(f"Unknown command: {args.cmd[0]}")

if __name__ == "__main__":
    main()
