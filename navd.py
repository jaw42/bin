#!/usr/bin/env python3
import curses
import os
import sys
from os import listdir
from os import path

window = 0
keys = {}
mesg = ''

class FileList:
    def __init__(self):
        self.cur_line = 1

    def get_paths(self, hidden):
        self.dict = []
        pwd = os.getcwd()
        self.dict.append({'path': os.getcwd(), 'ptype': 'aaaa'})
        for f in listdir(pwd):
            if not f.startswith('.') or hidden:
                if os.path.isdir(f):
                    self.dict.append({'path': f, 'ptype': 'dir'})
                elif os.path.isfile(f):
                    self.dict.append({'path': f, 'ptype': 'file'})

        self.dict = sorted(self.dict, key=lambda path: path['ptype'])

    def len(self):
        return len(self.dict)

    def get(self, n):
        return self.dict[n]

    def current(self):
        return self.get(self.cur_line)

    def draw(self, start=0, search='', window_line=-1, file_line=-1):
        global window
        global mesg

        if file_line >= 0:
            if file_line > window.getmaxyx()[0] - 2:
                start = file_line - 1

        self.start = start
        window.erase()

        num = window.getmaxyx()[0] - 1
        cursor_pos = 1
        screen_line = 0
        n = -1
        for item in self.dict:
            path = item['path']
            ptype = item['ptype']
            n += 1
            if n < start:
                continue
            elif screen_line == num:
                break
            if path == search:
                cursor_pos = screen_line
                search_line = n
                mesg = search

#             path = str(n) + '  ' + path
            if ptype == 'aaaa':
                window.addstr(screen_line, 0, path, curses.color_pair(2))
            elif ptype == 'dir':
                window.addstr(screen_line, 0, path + '/', curses.color_pair(1))
            else:
                window.addstr(screen_line, 0, path)
            screen_line += 1

        window.refresh()
        if file_line >= 0:
            self.cur_line = file_line
        elif window_line >= 0:
            window.move(window_line, 0)
        elif search:
            window.move(cursor_pos, 0)
            self.cur_line = search_line
        else:
            window.move(1, 0)
            self.cur_line = 1

    def redraw(self):
        self.draw(file_line=self.cur_line)

    def move(self, direction):
        aim = window.getyx()[0] + direction
        if aim < 0:
            aim = 0
            if self.cur_line + direction < 0:
                direction = 0

            self.cur_line += direction
            self.draw(start=self.start + direction)

        elif aim > window.getmaxyx()[0] - 2:
            aim = window.getmaxyx()[0] - 2
            if self.cur_line + direction >= self.len():
                direction = 0

            self.cur_line += direction
            self.draw(start=self.start + direction)

        elif aim > self.len() - 1:
            aim = window.getyx()[0]

        else:
            self.cur_line += direction

        window.move(aim, 0)

    def top(self):
        self.cur_line = 1
        self.draw()

    def bot(self):
        start = 0
        file_line = self.len() - 1
        if file_line > window.getmaxyx()[0]:
            start = self.len() - window.getmaxyx()[0]
            file_line = window.getmaxyx()[0] - 1
        self.cur_line = file_line
        self.draw(start=start, file_line=file_line)
        msg(self.cur_line)

# Setup the window
def setup_curses():
    global window
    window = curses.initscr()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

def goto_dir(path):
    path = os.path.join(os.getcwd(), path)
    os.chdir(path)

def msg(message):
    if not isinstance(message, str):
        message = str(message)

    (cur_y, cur_x) = window.getyx()
    (y, x) = window.getmaxyx()
    window.move(y-1, 0)
    window.clrtoeol()
    window.addstr(message)
    window.move(cur_y, 0)

def setup_keys():
    global keys
    keys['n'] = {}
    keys['n'][ord('G')] = '<cursor-bottom>'    # G
    keys['n'][ord('j')] = '<cursor-down>'      # j
    keys['n'][258]      = '<cursor-down>'      # DOWN
    keys['n'][4]        = '<cursor-jump-down>' # ^d
    keys['n'][21]       = '<cursor-jump-up>'   # ^u
    keys['n'][ord('k')] = '<cursor-up>'        # k
    keys['n'][259]      = '<cursor-up>'        # UP
    keys['n'][ord('l')] = '<descend>'          # l
    keys['n'][10]       = '<descend>'          # ENTER
    keys['n'][13]       = '<descend>'          # CR
    keys['n'][32]       = '<descend>'          # SPACE
    keys['n'][ord('?')] = '<help>'             # ?
    keys['n'][ord('-')] = '<parent>'           # -
    keys['n'][ord('h')] = '<parent>'           # h
    keys['n'][ord('q')] = '<quit>'             # q
    keys['n'][27]       = '<quit>'             # ESC
    keys['n'][ord('M')] = '<toggle-debug>'     # M
    keys['n'][ord('s')] = '<toggle-hidden>'    # s
    keys['n'][ord('g')] = '<g-mode>'           # g
    keys['g'] = {}
    keys['g'][ord('g')] = '<cursor-top>'       # g
    keys['g'][ord('h')] = '<goto-home>'        # H
    keys['g'][ord('t')] = '<goto-tmp>'        # H

def getcmd(key, mode='n'):
    global keys
    cmd = keys.get(mode, 'n').get(key, '<unknown>')
    msg(cmd)
    return cmd

def print_help():
    global keys
    lst = []
    for cmd, ops in keys.items():
        for key in ops:
            lst.append((cmd, key))

    lst = sorted(lst)
    window.clear()
    for line in lst:
        cmd = line[0]
        key = chr(line[1]).encode('unicode-escape').decode('utf-8')
        line = '{}: {}'.format(cmd, key)
        window.addstr(line + '\n')

    cmd = 0
    while cmd != '<quit>':
        key = window.getch()
        cmd = getcmd(key)

# Main
def main(stdscr):
    global window
    global mesg
    window = stdscr
    hidden = False
    debug = True
    setup_curses()
    setup_keys()

    filelist = FileList()
    filelist.get_paths(hidden)

    filelist.draw()
    window.move(1,0)

    cmd = 0
    subcmd = ''
    while cmd != '<quit>':
        if subcmd:
            cmd = subcmd
        else:
            key = window.getch()
            cmd = getcmd(key)
        window.refresh()
        cur_path = filelist.current()

        if cmd == '<toggle-hidden>':
            subcmd = ''
            old_file = filelist.current()['path']
            hidden = not hidden
            window.erase()
            filelist.get_paths(hidden)
            filelist.draw(search=old_file)

        elif cmd == '<cursor-up>':
            subcmd = ''
            filelist.move(-1)

        elif cmd == '<cursor-jump-up>':
            subcmd = ''
            filelist.move(-1 * int(window.getmaxyx()[0] / 2))

        elif cmd == '<cursor-down>':
            subcmd = ''
            filelist.move(1)

        elif cmd == '<cursor-jump-down>':
            subcmd = ''
            filelist.move(int(window.getmaxyx()[0] / 2))

        elif cmd == '<cursor-top>':
            subcmd = ''
            filelist.top()

        elif cmd == '<cursor-bottom>':
            subcmd = ''
            filelist.bot()

        elif cmd == '<descend>':
            subcmd = ''
            if cur_path['ptype'] == 'dir':
                goto_dir(cur_path['path'])
                filelist.get_paths(hidden)
                filelist.draw()
            else:
                break

        elif cmd == '<parent>':
            subcmd = ''
            cwd = os.getcwd()
            parent_path = os.path.dirname(cwd)
            goto_dir(parent_path)
            search_path = os.path.basename(cwd)
            if search_path.startswith('.'):
                hidden = True

            filelist.get_paths(hidden)
            filelist.draw(search=search_path)

        elif cmd == '<g-mode>':
            key = window.getch()
            subcmd = getcmd(key, mode='g')

        elif cmd.startswith('<goto-'):
            subcmd = ''
            envvar = cmd[6:-1].upper()
            os.chdir(os.environ[envvar])
            filelist.get_paths(hidden)
            filelist.draw()

        elif cmd == '<toggle-debug>':
            subcmd = ''
            debug = not debug

        elif cmd == '<help>':
            subcmd = ''
            print_help()
            filelist.redraw()

        elif key == curses.KEY_RESIZE:
            subcmd = ''
            filelist.redraw()

        elif cmd == '<unknown>':
            subcmd = ''
            pass

        if debug:
            key_str = chr(key).encode('unicode-escape').decode('utf-8')
            cur_line = filelist.cur_line
            current = filelist.current()['path']
            info = '{} {} {} {} {} {}'.format(mesg, key_str, key, cmd, cur_line, current)
            msg(info)

    msg(cur_path)
    print(cur_path)

# Handle main
if __name__ == '__main__':
    if len(sys.argv) > 1:
        if os.path.isdir(sys.argv[1]):
            os.chdir(sys.argv[1])
            print(sys.argv[1])
        else:
            print('Not a directory: ' + sys.argv[1])
    curses.wrapper(main)
