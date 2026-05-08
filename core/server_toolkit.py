#!/usr/bin/env python3

from core.plugin_loader import load_plugins

import argparse

def fatal(error):
    print(f"[FATAL] {error}")
    exit(1)

def start_CLI():
    print_plugins()

def start_TUI():
    print("TODO: TUI")

def print_plugins():
    plugins = load_plugins()

    for plugin in plugins:
        print(f"\n[{plugin.name}]")

        commands = plugin.commands()

        for idx, command in enumerate(commands):
            print(f"{idx+1}. {command}")

def arg_parsing():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cli", help="Launch CLI mode", action="store_true")
    parser.add_argument("-t", "--tui", help="Launch TUI mode", action="store_false")

    parser.add_argument("--plugin", help="Specify plugin that tool is from")
    parser.add_argument("--tool", help="Specify tool from plugin to run in terminal")

    args = parser.parse_args()
    if args.cli:
        start_CLI()
    elif args.tui:
        start_TUI()

def main():
    arg_parsing()

if __name__ == "__main__":
    main()