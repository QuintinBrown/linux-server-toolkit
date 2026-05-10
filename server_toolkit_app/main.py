from server_toolkit_app.plugin_loader import load_plugins

import argparse
import subprocess
import curses

def fatal(error):
    print(f"[FATAL] {error}")
    exit(1)

def error(description):
    print(f"[ERROR] {description}\n")

def quit():
    exit(0)

def clear():
    subprocess.run('clear')

def plugin_menu(plugin):
    clear()
    commands = plugin.commands()
    command_items = list(commands.items())

    while True:
        print(f"[{plugin.name}]")

        # print commands belonging to the plugin with index starting at 1
        for idx, (command_name, _) in enumerate(command_items, start=1):
            print(f"{idx}. {command_name}")
        print("b. Back to plugin selection")
        print("q. Quit")

        command_choice = input("\nSelect a tool ").strip()

        if command_choice.lower() == "q":
            quit()

        if command_choice.lower() == "b":
            clear()
            return
        
        try:
            command_index = int(command_choice) - 1
        except ValueError:
            clear()
            error(f"Invalid command option {command_choice}")
            continue

        if command_index < 0 or command_index > len(commands):
            clear()
            error(f"Invalid command option {command_choice}")
            continue

        command_name, command_func = command_items[command_index]

        # clears and runs the command, checks the return result and prints it
        clear()
        print(f"Running: {command_name}\n")

        result = command_func()

        if result is not None:
            print(result)
        
        input("\nPress Enter to continue...")
        clear()

def start_CLI():
    clear()
    plugins = load_plugins()
    while True:
        print("Available plugins")

        # Print list of plugins in order with index starting at 1
        for idx, plugin in enumerate(plugins, start=1):
            print(f"{idx}. {plugin.name}")

        print("q. Quit")

        plugin_choice = input("\nSelect plugin ").strip()

        if plugin_choice.lower() == "q":
            quit()
        
        try:
            plugin_index = int(plugin_choice) - 1
        except ValueError:
            clear()
            error(f"Invalid plugin option {plugin_choice}")
            continue

        if plugin_index < 0 or plugin_index > len(plugins):
            clear()
            error(f"Invalid plugin option {plugin_choice}")
            continue

        selected_plugin = plugins[plugin_index]
        plugin_menu(selected_plugin) # run the plugin menu for the selected plugin

def curses_main(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()

    plugins_begin_x = 2
    plugins_begin_y = 0
    plugins_height = curses.LINES - 20
    plugins_width = curses.COLS // 3


    plugins_win = curses.newwin(plugins_height, 
                                plugins_width, 
                                plugins_begin_y, 
                                plugins_begin_x
                            )
    
    commands_begin_x = plugins_begin_x + plugins_width + 1
    commands_width = curses.COLS - commands_begin_x - 1
    
    commands_win = curses.newwin(plugins_height, 
                                commands_width, 
                                plugins_begin_y, 
                                commands_begin_x
                            )
    
    output_begin_x = 2
    output_begin_y = plugins_height + plugins_begin_y
    output_width = curses.COLS - output_begin_x - 1
    output_height = curses.LINES - output_begin_y

    output_win = curses.newwin(output_height, 
                                output_width, 
                                output_begin_y, 
                                output_begin_x
                            )

    plugins = load_plugins()

    plugins_win.box()

    plugins_win.addstr(1, 1, "Available Plugins:")

    for idx, plugin in enumerate(plugins, start=1):
            plugins_win.addstr(idx + 1, 1, f"{idx}. {plugin.name}")
    
    plugins_win.addstr(len(plugins) + 2, 1, "q. quit")

    plugins_win.refresh()

    selected_plugin = plugins[1]
    commands = selected_plugin.commands()
    command_items = list(commands.items())

    commands_win.box()

    commands_win.addstr(1, 1, f"[{plugin.name}]")
    for idx, (command_name, _) in enumerate(command_items, start=1):
        commands_win.addstr(idx + 1, 1, f"{idx}. {command_name}")
    
    commands_win.addstr(len(command_items) + 1, 1, "b. Back to plugin selection")
    commands_win.addstr(len(command_items) + 2, 1, "q. Quit")
    commands_win.refresh()

    output_win.box()
    output_win.refresh()

    while True:
        ch = stdscr.getch()
        if ch == ord('q'):
            break

def start_TUI():
    curses.wrapper(curses_main)

def arg_parsing():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cli", help="Launch CLI mode", action="store_true")
    parser.add_argument("-t", "--tui", help="Launch TUI mode", action="store_true")

    parser.add_argument("--plugin", help="Specify plugin that tool is from")
    parser.add_argument("--tool", help="Specify tool from plugin to run in terminal")

    args = parser.parse_args()
    
    if not args.tui:
        start_CLI()
    else:
        start_TUI()

def main():
    arg_parsing()