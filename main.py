#!/usr/bin/env python3
import sys,os,json,re
assert sys.version_info >= (3,9), "This script requires at least Python 3.9"


def load(l):
    f = open(os.path.join(sys.path[0], l))
    data = f.read()
    j = json.loads(data)
    return j

def find_passage(game_desc, pid):
    for p in game_desc["passages"]:
        if p["pid"] == pid:
            return p
    return {}

# Removes Harlowe formatting from Twison description
def format_passage(description):
    description = re.sub(r'//([^/]*)//',r'\1',description)
    description = re.sub(r"''([^']*)''",r'\1',description)
    description = re.sub(r'~~([^~]*)~~',r'\1',description)
    description = re.sub(r'\*\*([^\*]*)\*\*',r'\1',description)
    description = re.sub(r'\*([^\*]*)\*',r'\1',description)
    description = re.sub(r'\^\^([^\^]*)\^\^',r'\1',description)
    #description = re.sub(r'(\[\[[^\|]*?)\|([^\]]*?\]\])',r'\1->\2',description)
    #description = re.sub(r'\[\[([^(->\])]*?)->[^\]]*?\]\]',r'[ \1 ]',description)
    description = re.sub(r'\[\[(.+?)\]\]','',description)
    return description

def update_score(current,score,locations):
    if "score" in current and current["name"] not in locations:
        score += int(current["score"])
    return score

def update(current,choice,game_desc):
    if choice == "":
        return current
    try:
        choice = int(choice)
        current = find_passage(game_desc, current["links"][choice-1]["pid"])
    except:
        print("I don't understand. Please try again.")
    #for l in current["links"]:
    #    if l["name"].lower() == choice:
    #        current = find_passage(game_desc, l["pid"])
    #        return current
    return current

def update_inventory(current,inventory,choice):
    if "inventory" in current:
        for i in current["inventory"]:
            if choice == "get {}".format(i):
                inventory.add(i)
    return choice

def render(current,score,moves):
    print("\n")
    print("Score: {score}     Moves: {moves}".format(score=score,moves=moves))
    print("\n")
    print(format_passage(current["text"]))
    option = 0
    if "links" in current:
        for l in current["links"]:
            option +=1
            print("{option}: {name}".format(option=option,name=l["name"]))
        print("\n")
    if "inventory" in current and len(current["inventory"]):
        print("You see ")
        for i in current["inventory"]:
            print(i)

def get_input():
    choice = input("What would you like to do? (Type quit to exit) ")
    choice = choice.lower().strip()
    return choice


def main():
    game_desc = load("game.json")
    current = find_passage(game_desc, game_desc["startnode"])
    last_location = current
    choice = ""

    score = 0
    moves = 0
    locations = set()

    while choice != "quit" and current != {}:
        current = update(current,choice,game_desc)
        locations.add(current["name"])
        score = update_score(current,score,locations)
        update(current,choice,game_desc)
        if current != last_location:
            moves += 1
            last_location = current
        render(current,score,moves)
        if "links" in current:
            choice = get_input()   
        else:
            current = {}
    print("Thanks for playing!")
    print("Your final score was {score} in {moves} moves.".format(score=score,moves=moves))



if __name__ == "__main__":
  main()