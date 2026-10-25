"""A tiny text adventure. Grow this world with your team!"""

ROOMS = {
    "hall": {
        "description": "You are in a quiet hall. A door leads north.",
        "exits": {"north": "garden"},
    },
    "garden": {
        "description": "You are in a garden full of strange flowers. The hall is to the south.",
        "exits": {"south": "hall"},
    },
}

ERRORS = {
   "no_exit": "You cannot go {direction} from here. Look at the room description for the exits.",
   "no_way": "You cannot go {direction} from here. Look at the room description for the exits.",
   "no_yay": "You cannot go {direction} from here. Look at the room description for the exits.",
}

def main():
    current = "hall"
    print("Welcome! Type 'go <direction>' to move, or 'quit' to stop.")
    while True:
        print()
        print(ROOMS[current]["description"])
        command = input("> ").strip().lower()
        if command == "quit":
            print("Goodbye!")
            break
        if command.startswith("go "):
            direction = command[3:]
            next_room = ROOMS[current]["exits"].get(direction)
            if next_room:
                current = next_room
            else:
                print("You cannot go that way.")
        else:
            print("I don't understand that.")


if __name__ == "__main__":
    main()
