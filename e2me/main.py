import argparse
import os
import shutil
import toml

from .send_email import send_email
from .receive_email import receive_email


CONFIG_NAME = "e2me.toml"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd", type=str, nargs="?", help="init run get")
    parser.add_argument("-c", "--config", help="config file path")
    parser.add_argument("-s", "--save", action="store_true", help="save config file")
    args = parser.parse_args()

    default_config_path = os.path.join(os.path.dirname(__file__), CONFIG_NAME)

    if args.cmd == "init":
        if os.path.exists(CONFIG_NAME):
            print(f"Config file already exists: {CONFIG_NAME}")
        else:
            # copy default config file
            shutil.copyfile(default_config_path, CONFIG_NAME)
            print(f"Config file created: {CONFIG_NAME}")
        return

    config_name = CONFIG_NAME
    if args.config:
        config_name = args.config

    if not os.path.exists(config_name):
        # print(f"Config file not found: {config_name}\n")
        # print("Please run 'e2me init' to create a new config file or use '-c' to specify the config file path.")
        # exit(1)
        config_name = default_config_path

    config = toml.load(config_name)

    if args.save:
        # replace default config file with new config
        print("Your current config is:")
        print("     email: " + config["email"]["email"])
        print("     passwd: " + config["email"]["passwd"] + "\n")
        
        if input("Saving config file and overwriting default config file(y/n)?") == "y":
            try:
                shutil.copyfile(config_name, default_config_path)
                print(f"Config file saved: {config_name}")
            except PermissionError:
                print("Permission denied. Please run the script with sudo.")
        else:
            print("Config file not saved.")

        return

    if args.cmd is None:
        # print help message
        parser.print_help()
        return

    if args.cmd == "run":
        send_email(config)
    elif args.cmd == "get":
        receive_email(config)
    else:
        print(f"Unknown command: {args.cmd}")

if __name__ == "__main__":
    main()
