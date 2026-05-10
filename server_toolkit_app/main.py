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

def draw_plugins(win, plugins, selected_index, active):
    win.clear()
    win.box()

    if active:
        win.attron(curses.A_REVERSE)
        win.addstr(1, 1, "[Available Plugins]")
        win.attroff(curses.A_REVERSE)
    else:
        win.addstr(1, 1, "[Available Plugins]")

    for idx, plugin in enumerate(plugins):
        line = f"{idx + 1}. {plugin.name}"

        if idx == selected_index:
            win.attron(curses.A_REVERSE)
            win.addstr(idx + 3, 1, line)
            win.attroff(curses.A_REVERSE)
        else:
            win.addstr(idx + 3, 1, line)
    
    #win.addstr(len(plugins) + 3, 1, "q. Quit")
    win.refresh()

def draw_commands(win, plugin, selected_index, active):
    win.clear()
    win.box()

    commands = plugin.commands()
    command_items = list(plugin.commands().items())

    if active:
        win.attron(curses.A_REVERSE)
        win.addstr(1, 1, f"[{plugin.name}]")
        win.attroff(curses.A_REVERSE)
    else:
        win.addstr(1, 1, f"[{plugin.name}]")

    for idx, (command_name, command_spec) in enumerate(command_items):
        is_interactive = (
            isinstance(command_spec, dict) and command_spec.get("interactive", False)
        )
        suffix = " *" if is_interactive else ""
        line = f"{idx + 1}. {command_name}{suffix}"

        if idx == selected_index:
            win.attron(curses.A_REVERSE)
            win.addstr(idx + 3, 1, line)
            win.attroff(curses.A_REVERSE)
        else:
            win.addstr(idx + 3, 1, line)            
    
    win.refresh()

def draw_output(win, text=""):
    win.clear()
    win.box()
    win.addstr(1, 1, "[Output]")

    lines = str(text).splitlines() or [""]

    max_y, max_x = win.getmaxyx()
    for idx, line in enumerate(lines[: max_y - 3]):
        win.addstr(idx + 2, 1, line[: max_x - 2])
    
    win.refresh()

def curses_main(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()
    stdscr.keypad(True)

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

    output_lines = []

    def curses_output(text):
        output_lines.append(str(text))
        draw_output(output_win, "\n".join(output_lines))
    
    plugins = load_plugins(output_func=curses_output)

    active_pane = "plugins"
    plugin_index = 0
    commands_index = 0
    output = ""

    selected_plugin = plugins[plugin_index]
    
    draw_plugins(plugins_win, plugins, plugin_index, active_pane == "plugins")
    draw_commands(commands_win, selected_plugin, commands_index, active_pane == "commands")
    draw_output(output_win)
    
    while True:
        key = stdscr.getch()

        selected_plugin = plugins[plugin_index]
        command_items = list(selected_plugin.commands().items())

        if key == ord('q'):
            break
        elif key == ord('\t'):
            active_pane = "commands" if active_pane == "plugins" else "plugins"
        elif key == curses.KEY_UP:
            if active_pane == "plugins":
                plugin_index = max(0, plugin_index - 1)
                commands_index = 0
            else:
                commands_index = max(0, commands_index - 1)
        elif key == curses.KEY_DOWN:
            if active_pane == "plugins":
                plugin_index = min(len(plugins) - 1, plugin_index + 1)
                commands_index = 0
            else:
                commands_index = min(len(command_items) - 1, commands_index + 1)
        elif key in (curses.KEY_ENTER, 10, 13):
            if active_pane == "commands" and command_items:
                command_name, command_spec = command_items[commands_index]
                
                if isinstance(command_spec, dict):
                    command_func =  command_spec["func"]
                    needs_terminal = command_spec.get("interactive", False)
                else:
                    command_func = command_spec
                    needs_terminal = False
                
                output_lines.clear()
                draw_output(output_win)

                try:
                    if needs_terminal:
                        curses.nocbreak()
                        stdscr.keypad(False)
                        curses.echo()
                        curses.endwin()
                        clear()

                        try:
                            result = command_func()
                            input("\nPress Enter to return to the TUI")
                        finally:
                            curses.noecho()
                            curses.cbreak()
                            stdscr.keypad(True)
                            stdscr.clear()
                            stdscr.refresh()

                        output_lines.clear()
                        curses_output(f"Returned from: {command_name}")
                    else:
                        curses_output(f"Running: {command_name}")

                        result = command_func()

                        if result is not None:
                            curses_output(result)

                except Exception as exc:
                    curses_output(f"[ERROR] {exc}")
                
        else:
            continue

        selected_plugin = plugins[plugin_index]
        draw_plugins(plugins_win, plugins, plugin_index, active_pane == "plugins")
        draw_commands(commands_win, selected_plugin, commands_index, active_pane == "commands")

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