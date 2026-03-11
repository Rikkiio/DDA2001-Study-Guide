#!/usr/bin/env python3
"""
CSC1002 Console-Based Editor
A simple text-based editor following the assignment requirements.
Uses only functions (no classes) as specified.
"""

import re

# Global variables (no class)
text_content = ""
cursor_pos = 0
show_cursor = True


def display_help():
    """Display the help menu."""
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
    print("dw - delete word at or after cursor")
    print("v - view editor content")
    print("q - quit program")


def print_content():
    """Print the editor content and cursor if enabled."""
    global text_content, cursor_pos, show_cursor
    
    if not text_content:
        print()
    elif not show_cursor:
        print(text_content)
    else:
        # Ensure cursor position is valid
        if cursor_pos >= len(text_content):
            cursor_pos = max(0, len(text_content) - 1)
        if cursor_pos < 0:
            cursor_pos = 0
        
        left = text_content[:cursor_pos]
        char = text_content[cursor_pos] if cursor_pos < len(text_content) else ""
        right = text_content[cursor_pos + 1:]
        print(f"{left}\033[42m{char}\033[0m{right}")


def toggle_cursor():
    """Toggle the row cursor on and off."""
    global show_cursor
    show_cursor = not show_cursor


def move_left():
    """Move cursor one position to the left."""
    global cursor_pos
    cursor_pos = max(0, cursor_pos - 1)


def move_right():
    """Move cursor one position to the right."""
    global cursor_pos, text_content
    if text_content:
        cursor_pos = min(len(text_content) - 1, cursor_pos + 1)


def move_home():
    """Move cursor to the beginning of the line."""
    global cursor_pos
    cursor_pos = 0


def move_end():
    """Move cursor to the end of the line."""
    global cursor_pos, text_content
    cursor_pos = max(0, len(text_content) - 1)


def get_word_spans():
    """Return a list of (start, end) tuples for all words."""
    global text_content
    return [(m.start(), m.end() - 1) for m in re.finditer(r'\S+', text_content)]


def move_next_word():
    """Move to the beginning of the next word."""
    global cursor_pos
    for start, _ in get_word_spans():
        if start > cursor_pos:
            cursor_pos = start
            return
    move_end()


def move_prev_word():
    """Move to the beginning of the current or previous word."""
    global cursor_pos
    for start, _ in reversed(get_word_spans()):
        if start < cursor_pos:
            cursor_pos = start
            return
    move_home()


def move_end_word():
    """Move to the end of the current or next word."""
    global cursor_pos
    for _, end in get_word_spans():
        if end > cursor_pos:
            cursor_pos = end
            return
    move_end()


def insert_text(text):
    """Insert text before cursor."""
    global text_content, cursor_pos
    text_content = text_content[:cursor_pos] + text + text_content[cursor_pos:]


def append_text(text):
    """Append text after cursor."""
    global text_content, cursor_pos
    pos = cursor_pos + 1
    text_content = text_content[:pos] + text + text_content[pos:]
    cursor_pos = pos + len(text) - 1


def insert_front(text):
    """Insert text from the beginning."""
    move_home()
    insert_text(text)


def append_end(text):
    """Append text at the end."""
    move_end()
    append_text(text)


def delete_char():
    """Delete the character at the cursor."""
    global text_content, cursor_pos
    if not text_content:
        return
    text_content = text_content[:cursor_pos] + text_content[cursor_pos + 1:]
    cursor_pos = min(cursor_pos, max(0, len(text_content) - 1))


def delete_prev_char():
    """Delete the character before the cursor."""
    global text_content, cursor_pos
    if not text_content or cursor_pos == 0:
        return
    text_content = text_content[:cursor_pos - 1] + text_content[cursor_pos:]
    cursor_pos -= 1


def delete_word():
    """Delete the word at or after cursor (dw command)."""
    global text_content, cursor_pos
    if not text_content:
        return
    
    spans = get_word_spans()
    for start, end in spans:
        if start >= cursor_pos:
            # Delete from start to end (inclusive)
            text_content = text_content[:start] + text_content[end + 1:]
            cursor_pos = min(cursor_pos, max(0, len(text_content) - 1))
            return
    
    # No more words, move to end
    move_end()


def exec_no_arg(cmd):
    """Execute single character commands without extra text."""
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
        'dw': delete_word,
    }
    if cmd in funcs:
        funcs[cmd]()
        return True
    return False


def exec_text_arg(cmd, text):
    """Execute commands that require extra text input."""
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
    """
    Process user input, route to correct function.
    Returns True if content should be displayed after execution.
    """
    # Help command
    if user_in == '?':
        display_help()
        return False
    
    # Quit command (handled in main)
    if user_in == 'q':
        return True
    
    # Check for two-letter command first (dw)
    if len(user_in) == 2 and user_in == 'dw':
        return exec_no_arg(user_in)
    
    # Single character commands
    if len(user_in) == 1:
        return exec_no_arg(user_in)
    
    # Commands with text argument (i, a, I, A)
    if len(user_in) > 1:
        cmd = user_in[0]
        text = user_in[1:]  # Everything after first character
        if cmd in ['i', 'a', 'I', 'A']:
            return exec_text_arg(cmd, text)
    
    # Invalid command
    return False


def main():
    """Main program entry point."""
    display_help()
    print()
    
    while True:
        try:
            user_in = input(">")
        except EOFError:
            break
        
        if user_in == 'q':
            break
        
        if process_input(user_in):
            print_content()


if __name__ == "__main__":
    main()
