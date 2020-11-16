import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# define a function that checks if the spell can be cast
def can_cast(spell_list, inv_list):
    if spell_list[-1] == 0: # checks if spell castable
        return False
    elif sum(inv_list[0]) + sum(spell_list[1]) > 10: # checks if inv full
        return False
    # check if the inv has the ingredients to cast the spell
    for i in range(4):
        if spell_list[1][i] + inv_list[0][i] < 0:
            return False
    return True

# define a function that checks if the potion can be brewed
def can_brew(potion_list, inv_list):
    # check if inv has the ingredients to brew the potion
    for i in range(4):
        if potion_list[1][i] + inv_list[0][i] < 0:
            return False
    return True

# game loop
while True:
    brew = [] # empty list for potions_lists
    cast = [] # empty list for spells_lists
    inv = [] # empty list for inv_list
    rup = [] # empty list for current score

    action_count = int(input())  # the number of spells and recipes in play
    for i in range(action_count):
        # action_id: the unique ID of this spell or recipe
        # action_type: in the first league: BREW; later: CAST, OPPONENT_CAST, LEARN, BREW
        # delta_0: tier-0 ingredient change
        # delta_1: tier-1 ingredient change
        # delta_2: tier-2 ingredient change
        # delta_3: tier-3 ingredient change
        # price: the price in rupees if this is a potion
        # tome_index: in the first two leagues: always 0; later: the index in the tome if this is a tome spell, equal to the read-ahead tax; For brews, this is the value of the current urgency bonus
        # tax_count: in the first two leagues: always 0; later: the amount of taxed tier-0 ingredients you gain from learning this spell; For brews, this is how many times you can still gain an urgency bonus
        # castable: in the first league: always 0; later: 1 if this is a castable player spell
        # repeatable: for the first two leagues: always 0; later: 1 if this is a repeatable player spell
        action_id, action_type, delta_0, delta_1, delta_2, delta_3, price, tome_index, tax_count, castable, repeatable = input().split()
        action_id = int(action_id)
        delta_0 = int(delta_0)
        delta_1 = int(delta_1)
        delta_2 = int(delta_2)
        delta_3 = int(delta_3)
        price = int(price)
        tome_index = int(tome_index)
        tax_count = int(tax_count)
        castable = castable != "0"
        repeatable = repeatable != "0"
        
        # Loads list of potions
        if action_type == 'BREW':
            brew.append([action_id, [delta_0, delta_1, delta_2, delta_3], price])
        elif action_type == "CAST":
            cast.append([action_id, [delta_0, delta_1, delta_2, delta_3], castable])

    for i in range(2):
        # inv_0: tier-0 ingredients in inventory
        # score: amount of rupees
        inv_0, inv_1, inv_2, inv_3, score = [int(j) for j in input().split()]
        # load in mine and enemies inventory
        inv.append([inv_0, inv_1, inv_2, inv_3])
        rup.append(score)
    
    # Write an action using print
    # to debug: print("Debug messages...", file=sys.stderr, flush=True)
    
    rest = False # Assume to not rest
    cast_it = False # Assume to not cast spell
    
    # Loop round the brew spells searching for max price
    maxprice = [0]
    for potion in brew: 
        if potion[-1] > maxprice[-1]:
            maxprice = potion

    # casts spells to make the chosen potion
    if can_brew(maxprice, inv) == False: # check if need to cast a spell
        # rest if we cant cast a spell
        rest = True
        # check what ingredient i need more of
        for i in range(4):
            if maxprice[1][i] + inv[0][i] < 0:
                need_more = i
        # loop round ingredients, updating the need_more to a less expensive ingredient
        for _ in range(need_more, -1, -1):
            # check spells if they can provide me with more of that
            for spell in cast[::-1]:
                if spell[1][_] > 0 and can_cast(spell, inv):
                    # if we cast a spell we break the loops and do it
                    cast_it = True
                    best_spell = spell
                    break
            if cast_it:
                break


    if cast_it:
        print(f"CAST {best_spell[0]}")
    elif rest:
        print("REST")
    else:
        print(f"BREW {maxprice[0]}")
    # in the first league: BREW <id> | WAIT; later: BREW <id> | CAST <id> [<times>] | LEARN <id> | REST | WAIT