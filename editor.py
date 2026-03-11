#!/usr/bin/env python3
# CSC1002 Assignment 1 - Console Editor
# Student implementation

import re

# global variables for editor state
text_content = ""
cursor_pos = 0
show_cursor = True


def display_help():
    # show all available commands
    print("? - display this help info")
    print(". - toggle row cursor on and off")
    print("h - move cursor left")
    print("l - move cursor right")
    print("^ - move cursor to beginning of the line")
    print("$ - move cursor to end of the line")
    print("w - move cursor to beginning of next word")
    print("b - move cursor to beginning of current or previous word")
    print("e - move cursor to end of the word")
    print("i - insert <text> before cursor")
    print("a - append <text> after cursor")
    print("I - insert <text> from beginning")
    print("A - append <text> at the end")
    print("x - delete character at cursor")
    print("X - delete character before cursor")
    print("v - view editor content")
    print("q - quit program")


def print_content():
    # display current text with cursor highlighted
    global text_content, cursor_pos, show_cursor
    
    if not text_content:
        # empty text
        print()
    elif not show_cursor:
        # cursor hidden
        print(text_content)
    else:
        # make sure cursor is in valid range
        if cursor_pos >= len(text_content):
            cursor_pos = max(0, len(text_content) - 1)
        if cursor_pos < 0:
            cursor_pos = 0
        
        # split text around cursor position
        left = text_content[:cursor_pos]
        char = text_content[cursor_pos] if cursor_pos < len(text_content) else ""
        right = text_content[cursor_pos + 1:]
        # use ANSI color to highlight cursor
        print(f"{left}\033[42m{char}\033[0m{right}")


def toggle_cursor():
    # switch cursor display on/off
    global show_cursor
    show_cursor = not show_cursor


def move_left():
    # h command - move cursor left
    global cursor_pos
    # don't go below 0
    cursor_pos = max(0, cursor_pos - 1)


def move_right():
    # l command - move cursor right
    global cursor_pos, text_content
    
    # check if text is empty first
    if not text_content:
        return
    
    # move right but stay in bounds
    if cursor_pos < len(text_content) - 1:
        cursor_pos = cursor_pos + 1


def move_home():
    # ^ command - go to start of line
    global cursor_pos
    cursor_pos = 0


def move_end():
    # $ command - go to end of line
    global cursor_pos, text_content
    cursor_pos = max(0, len(text_content) - 1)


def get_word_spans():
    # find all word positions in text
    # returns list of (start, end) tuples
    global text_content
    return [(m.start(), m.end() - 1) for m in re.finditer(r'\S+', text_content)]


def move_next_word():
    # w command - jump to next word
    global cursor_pos
    spans = get_word_spans()
    
    # find first word that starts after cursor
    for start, _ in spans:
        if start > cursor_pos:
            cursor_pos = start
            return
    
    # no more words, go to end
    move_end()


def move_prev_word():
    # b command - jump to previous word
    global cursor_pos
    spans = get_word_spans()
    
    # search backwards
    for start, _ in reversed(spans):
        if start < cursor_pos:
            cursor_pos = start
            return
    
    # already at first word, go to start
    move_home()


def move_end_word():
    # e command - go to end of current word
    global cursor_pos
    spans = get_word_spans()
    
    # find word that contains or is after cursor
    for _, end in spans:
        if end > cursor_pos:
            cursor_pos = end
            return
    
    # no words found, go to end
    move_end()


def insert_text(text):
    # i command - insert before cursor
    global text_content, cursor_pos
    text_content = text_content[:cursor_pos] + text + text_content[cursor_pos:]


def append_text(text):
    # a command - append after cursor
    global text_content, cursor_pos
    pos = cursor_pos + 1
    text_content = text_content[:pos] + text + text_content[pos:]
    cursor_pos = pos + len(text) - 1


def insert_front(text):
    # I command - insert at beginning
    move_home()
    insert_text(text)


def append_end(text):
    # A command - append at end
    move_end()
    append_text(text)


def delete_char():
    # x command - delete char at cursor
    global text_content, cursor_pos
    
    if not text_content:
        return
    
    # remove character at cursor position
    text_content = text_content[:cursor_pos] + text_content[cursor_pos + 1:]
    
    # adjust cursor if needed
    cursor_pos = min(cursor_pos, max(0, len(text_content) - 1))


def delete_prev_char():
    # X command - delete char before cursor
    global text_content, cursor_pos
    
    # can't delete if at start or text is empty
    if not text_content or cursor_pos == 0:
        return
    
    # remove character before cursor
    text_content = text_content[:cursor_pos - 1] + text_content[cursor_pos:]
    cursor_pos -= 1


def exec_no_arg(cmd):
    # handle commands that don't need extra text
    funcs = {
        '.': toggle_cursor,
        'h': move_left,
        'l': move_right,
        '^': move_home,
        '$': move_end,
        'w': move_next_word,
        'b': move_prev_word,
        'e': move_end_word,
        'x': delete_char,
        'X': delete_prev_char,
        'v': lambda: None,
    }
    
    if cmd in funcs:
        funcs[cmd]()
        return True
    return False


def exec_text_arg(cmd, text):
    # handle commands that need text argument (i, a, I, A)
    funcs = {
        'i': insert_text,
        'a': append_text,
        'I': insert_front,
        'A': append_end,
    }
    
    if cmd in funcs:
        funcs[cmd](text)
        return True
    return False


def process_input(user_in):
    # parse and execute user command
    # return True if we should display content after
    
    # help command - show menu
    if user_in == '?':
        display_help()
        return False
    
    # quit - handled in main loop
    if user_in == 'q':
        return True
    
    # single char commands
    if len(user_in) == 1:
        return exec_no_arg(user_in)
    
    # commands with text: i, a, I, A
    # everything after first char is the text
    if len(user_in) > 1:
        cmd = user_in[0]
        text = user_in[1:]
        if cmd in ['i', 'a', 'I', 'A']:
            return exec_text_arg(cmd, text)
    
    # unknown command
    return False


def main():
    # main program loop
    while True:
        try:
            user_in = input(">")
        except EOFError:
            break
        
        if user_in == 'q':
            break
        
        # execute command and show result
        if process_input(user_in):
            print_content()


if __name__ == "__main__":
    main()
