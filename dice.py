import Descent_dice as dd

INSTRUCTIONS = """List the dice to roll separated by spaces. Possible die colors are:
    r = red
    bl = blue
    y = yellow
    g = gray
    bk = black
    br = brown
Other commands are:
    -v   toggle printing each die or just total on roll
    -h   display instructions
    -q   quit XXXXXX
"""
red = dd.Dice("red")
blue = dd.Dice("blue")
yellow = dd.Dice("yellow")
gray = dd.Dice("gray")
black = dd.Dice("black")
brown = dd.Dice("brown")

DIE_COLORS = {"r":red, "bl":blue, "y":yellow, "g":gray, "bk":black, "br":brown}
verbose = True

def print_instructions():
    print(INSTRUCTIONS)

def toggle_verbose():
    global verbose
    verbose = not verbose
    str = ""
    if verbose:
        str = "Printing all dice"
    else:
        str = "Printing total only"
    print(str)

COMMANDS = {"-h":print_instructions, "-v":toggle_verbose}
if __name__ == "__main__":
    print(INSTRUCTIONS)
    running = True
    while(running):
        print("Enter dice colors:")
        commands = raw_input()
        commands = commands.split(" ")
        dice = []
        for command in commands:
            if command in DIE_COLORS:
                dice.append(DIE_COLORS[command])
            elif command in COMMANDS:
                COMMANDS[command]()
            else:
                running = False
        if running:
            dd.Dice.roll_dice(dice, disp = verbose)
        else:
            print("Exiting ...")
