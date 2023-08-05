# pylint: disable=invalid-name,line-too-long
import os
from base64 import b64decode
from socket import gethostbyname
from webbrowser import open_new_tab
from requests import get

from colorama import Fore

from .menu import set_readline, tools_cli
from .config import INSTALL_DIR, GITHUB_PATH
from .hosts import get_hosts, add_host
from .utility import Utility


class host2ip(Utility):
    def __init__(self):
        super().__init__(description="Gets IP from host")

    def run(self):
        hosts = get_hosts()
        set_readline(hosts)
        user_host = input("\nEnter a host: ").strip()
        if not user_host in hosts:
            add_host(user_host)
        ip = gethostbyname(user_host)
        print(f"\n{user_host} has the IP of {ip}")


class base64_decode(Utility):
    def __init__(self):
        super().__init__(description="Decodes base64")

    def run(self):
        user_base64 = input("\nEnter base64: ").strip()
        text = b64decode(user_base64)
        print(f"\nDecoded that is: {text}")


class spawn_shell(Utility):
    def __init__(self):
        super().__init__(description="Spawns a local shell")

    def run(self):
        print("Enter `exit` to return to fsociety")
        shell = os.getenv("SHELL", "/bin/bash")
        os.chdir(INSTALL_DIR)
        os.system(shell)


class suggest_tool(Utility):
    def __init__(self):
        super().__init__(description="Suggest a tool or utility")

    def run(self):
        open_new_tab(
            f"https://github.com/{GITHUB_PATH}/issues/new?assignees=&labels=tool&template=---tool-request.md&title="
        )


class print_contributors(Utility):
    def __init__(self):
        super().__init__(description="Prints the usernames of our devs")

    def run(self):
        print(Fore.RED + """
    8888b.  888888 Yb    dP .dP"Y8 
    8I  Yb 88__    Yb  dP  `Ybo." 
    8I  dY 88""     YbdP   o.`Y8b 
    8888Y"  888888    YP    8bodP'
    """)
        response = get(
            f"https://api.github.com/repos/{GITHUB_PATH}/contributors")
        contributors = response.json()
        for contributor in sorted(contributors,
                                  key=lambda c: c['contributions'],
                                  reverse=True):
            username = contributor.get("login")
            print(f" {username} ".center(30, "-"))
        print(Fore.RESET)


__tools__ = [
    tool() for tool in
    [host2ip, base64_decode, spawn_shell, suggest_tool, print_contributors]
]


def cli():
    tools_cli(__name__, __tools__)
