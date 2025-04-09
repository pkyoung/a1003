#!/usr/bin/env python3
"""
This script normalizes text to compute Word Error Rate (WER). 
It provides options to:
- Convert text to uppercase.
- Remove punctuation marks (.,?!). (default: True)
- Remove strings enclosed in parentheses. (default: True)
- Remove specific words, characters, or strings. (default: None)
- Remove characters based on custom regular expressions. (default: None)
- Split words into individual characters.(default: False)
"""

import argparse
import sys
import re


def subline(
    line, remove_words=[], remove_char="", remove_string=[], regexps=[], toupper=True
):
    for w in remove_string:
        line = line.replace(w, "")

    if len(remove_char) > 0:
        line = re.sub(f"[{remove_char}]", " ", line)

    if len(remove_words) > 0:
        words = line.split()
        new_words = [word for word in words if word not in remove_words]
        line = " ".join(new_words)

    for reg, rep in regexps:
        line = reg.sub(rep, line)

    if toupper:
        line = line.upper()

    return line


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "infile",
        metavar="FILE",
        nargs="?",
        type=argparse.FileType("r"),
        default=sys.stdin,
        help="input filename",
    )
    parser.add_argument("-s", "--split-char", action="store_true", help="split char")
    parser.add_argument(
        "--remove-string", type=str, default="", help="strings to remove"
    )
    parser.add_argument("--remove-word", type=str, default="", help="words to remove")
    parser.add_argument(
        "--remove-re", type=str, action="append", default=None, help="reg exp to remove"
    )
    parser.add_argument("--remove-char", type=str, default="", help="chars to remove")
    parser.add_argument(
        "--remove-punct",
        action="store_true",
        default=True,
        help="Remove {.,?!} before white-space (default: True)",
    )
    parser.add_argument(
        "--no-remove-punct",
        action="store_false",
        dest="remove_punct",
        help="Do not remove {.,?!} before white-space",
    )
    parser.add_argument(
        "--remove-paren",
        action="store_true",
        default=True,
        help="Remove parentheses and their contents (default: True)",
    )
    parser.add_argument(
        "--no-remove-paren",
        action="store_false",
        dest="remove_paren",
        help="Do not remove parentheses and their contents",
    )

    args = parser.parse_args()

    remove_word = args.remove_word.split(",")
    remove_string = args.remove_string.split(",")

    regexps = []
    if args.remove_paren:
        regexps.append((re.compile(r"\([^)]*\)"), r""))
    if args.remove_punct:
        regexps.append((re.compile(r"[.,?!]+(\s|$)"), r"\1"))

    for line in args.infile:
        line = line.strip()
        header, *nline = line.split(None, 1)
        if len(nline) == 0:
            print(header)
        else:
            line = subline(
                " ".join(nline), remove_word, args.remove_char, remove_string, regexps
            )
            if args.split_char:
                print(header, " ".join(list("".join(line.split()))))
            else:
                print(header, " ".join(line.split()))


if __name__ == "__main__":
    main()
