# pylint: disable=unused-import,broad-except
import os
import shutil

from colorama import Fore, Back, Style

from fsociety.core.config import INSTALL_DIR

BACK_COMMANDS = ["exit", "back", "return"]


class CommandCompleter():
    def __init__(self, options):
        self.options = sorted(options)
        self.matches = list()

    def complete(self, text, state):
        response = None
        if state == 0:
            if text:
                self.matches = [
                    s for s in self.options if s and s.startswith(text)
                ]
            else:
                self.matches = self.options[:]
        try:
            response = self.matches[state]
        except IndexError:
            response = None
        return response


def set_readline(items):
    try:
        import readline
    except ImportError:
        pass
    else:
        import rlcompleter
        if isinstance(items, list):
            readline.set_completer(CommandCompleter(items).complete)
        elif isinstance(items, dict):
            readline.set_completer(CommandCompleter(items.keys()).complete)
        else:
            readline.set_completer(CommandCompleter(list(items)).complete)
        readline.parse_and_bind("tab: complete")


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def format_menu_item(item):
    string = str(item)
    if hasattr(item, "description") and item.description:
        string += f" - {item.description}"
    return f"{Back.WHITE}{Fore.BLACK}{string}{Style.RESET_ALL}"


def format_tools(tools):
    etc = False
    if len(tools) > 3:
        tools = tools[:3]
        etc = True
    res = "".join([f"\n\t{str(tool)}" for tool in tools])
    if etc:
        res += "\n\t..."
    return res


def module_name(module):
    return module.__name__.split(".")[-1]


def prompt(path="", base_path="~"):
    return f"{Fore.RED}fsociety {os.path.join(base_path, path, '')}#{Fore.WHITE} "


def input_wait():
    input("\nPress [ENTER] to continue... ")


def tools_cli(name, tools):
    tools_dict = dict()
    for tool in tools:
        tools_dict[str(tool)] = tool
        print(f"{format_menu_item(tool)}\n")
    print(f"{format_menu_item(str('back'))}\n")
    set_readline(list(tools_dict.keys()) + BACK_COMMANDS)
    selected_tool = input(prompt(name.split(".")[-2])).strip()
    if not selected_tool in tools_dict.keys():
        if selected_tool in BACK_COMMANDS:
            return
        print(f"{Fore.YELLOW}Invalid Command{Fore.RESET}")
        return
    tool = tools_dict.get(selected_tool)
    if hasattr(tool, "install") and not tool.installed():
        tool.install()
    try:
        response = tool.run()
        if response and response > 0:
            raise Exception
    except KeyboardInterrupt:
        return
    except Exception as error:
        print(f"{Fore.RED + selected_tool} failed{Fore.RESET}")
        print(str(error))
        if hasattr(tool, "install") and confirm("Do you want to reinstall?"):
            os.chdir(INSTALL_DIR)
            shutil.rmtree(tool.full_path)
            tool.install()
    input_wait()


def confirm(message="Do you want to?"):
    response = input(f"{message} (y/n): ").lower()
    if response:
        return response[0] == "y"
    return False
