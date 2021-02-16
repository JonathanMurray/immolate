#!/usr/bin/env python3
with open("files/spr_robot", "wb") as file:
    sprite = \
        ("XXXXXXXXXXXXXXXX"
         "X              X"
         "X XXXXX  XXXXX X"
         "X X   X  X   X X"
         "X X X X  X X X X"
         "X X   X  X   X X"
         "X XXXXX  XXXXX X"
         "X              X"
         "XXXXXXXXXXXXXXXX"
         "X   X   X   X  X"
         "X   X   X   X  X"
         "X   X   X   X  X"
         "X   X   X   X  X"
         "X   X   X   X  X"
         "X   X   X   X  X"
         "XXXXXXXXXXXXXXXX")

    for c in sprite:
        if c == "X":
            file.write(b"\xFF")
        else:
            file.write(b"\x00")

with open("files/spr_hero", "wb") as file:
    sprite = \
        ("XXXXXXXXXXXXXXXX"
         "X              X"
         "X XXXXX  XXXXX X"
         "X X   X  X   X X"
         "X X   X  X   X X"
         "X X   X  X   X X"
         "X XXXXX  XXXXX X"
         "X              X"
         "XXXXXXXXXXXXXXXX"
         "X              X"
         "X X          X X"
         "X  X        X  X"
         "X   XXXXXXXX   X"
         "X              X"
         "X              X"
         "XXXXXXXXXXXXXXXX")

    for c in sprite:
        if c == "X":
            file.write(b"\xFF")
        else:
            file.write(b"\x00")
