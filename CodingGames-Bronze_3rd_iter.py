import sys
import math

# define the number of round and number of brewed
brewed = 0
enemy_brewed = [0, 0]
round_i = 0

best_potion = 'nothing' # define best potion, that only gets changed if the potion isnt brewed anymore

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

# Define a function that checks if the potion can be learned
def can_learn(spell_list, inv_list):
    # if the tome_count > inventory + taxcount can't learn spell
    if spell_list[-1] > inv_list[0][0] + spell_list[-2]:
        return False
    else:
        return True


# Define a function to check if a potion is in the list of potions
def in_brew(a_potion, brew_list):
    for i in range(len(brew_list)):
        if a_potion[0] == brew_list[i][0]:
            return True
    return False

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
# game loop
while True:
    
    round_i += 1 # Tells us the round we are on
    brew = [] # empty list for potion_lists
    cast = [] # empty list for spell_lists
    learn = [] # empty list for spell_lists
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
        
        # Loads list of potions, spells and learning spells
        if action_type == 'BREW':
            brew.append([action_id, [delta_0, delta_1, delta_2, delta_3], tome_index, price])
        elif action_type == "CAST":
            cast.append([action_id, [delta_0, delta_1, delta_2, delta_3], repeatable, castable])
        elif action_type == "LEARN":
            learn.append([action_id, [delta_0, delta_1, delta_2, delta_3], repeatable, tax_count, tome_index])

    for i in range(2):
        # inv_0: tier-0 ingredients in inventory
        # score: amount of rupees
        inv_0, inv_1, inv_2, inv_3, score = [int(j) for j in input().split()]
        # load in mine and enemies inventory
        inv.append([inv_0, inv_1, inv_2, inv_3])
        rup.append(score)
    
    # Write an action using print
    # to debug: print("Debug messages...", file=sys.stderr, flush=True)

    # check if opponent has brewed and count it
    if rup[1] > enemy_brewed[1]:
        enemy_brewed[0] += 1
        enemy_brewed[1] = rup[1]
    
    brew_it = False # Assume to not brew
    rest_it = False # Assume to not rest
    cast_it = False # Assume to not cast spell
    learn_it = False # Assume to not learn spell
    defo_learn_it = False # Assume to not defo learn it


    # on the first 5 turns learn a spell
    if round_i in range(5):
        for spell in learn[::-1]:
            if can_learn(spell, inv):
                defo_learn_it = True
                best_learn = spell

    # # Loop round the brew spells searching for max price
    # best_potion = [0, 0, 0, 0]
    # for potion in brew: 
    #     if potion[-1] > best_potion[-1]:
    #         best_potion = potion
    
    # if not in_brew(best_potion, brew): # Checks if we need to revise the best potion to brew
    # Find the potion with the highest price to ease to make ratio
    diff_index = [0.1, 0.8, 1.8, 2.8] # TO IMPROVE // change the diff index depending on spells you can cast
    weighted = [] # make a list to score the potions on the ratio of how many rupies they give you : how hard they are to make with ingredients you have (higher the score the better)
    for potion in brew:
        weight = 0
        for i in range(4):
            if inv[0][i] < -potion[1][i]: # Check if we have enough ingredients, if enough=> difficulty to make is 0 so we pass
                weight += -(potion[1][i] + inv[0][i]) * diff_index[i] # negative number takes into account negative potion deltas
        if weight == 0:
            weighted.append(100)
        else:
            weighted.append(potion[-1]/weight) # price / difficulty to make 
    # print(f"debug ... {weighted}", file=sys.stderr, flush=True)
    best_potion = brew[weighted.index(max(weighted))]

    # If its the 5th brew, check if there is a quickest potion to make that beats enemy score and make it
    if brewed == 5 or enemy_brewed[0] == 5:
        # Same code as finding best potion to pass method
        diff_index = [0, 1, 2, 3]
        weighted = []
        for potion in brew:
            weight = 0
            for i in range(4):
                if inv[0][i] < -potion[1][i]:
                    weight += -(potion[1][i] + inv[0][i]) * diff_index[i]
            # append to weighted the potion list and the weight
            weighted.append([potion, weight])
        # print(f"debug ... {weighted}", file=sys.stderr, flush=True)  
        min_weight = 1000 # try and find the minimum weighted potion to brew that overtakes the enemy score
        for option in weighted:
            if option[0][-1] > rup[1]-rup[0]: # if the options price overtakes
                if option[1] < min_weight:
                    min_weight = option[1]
                    best_potion = option[0]
        # if best potion still not found pick the one with the highest score

    
    # IF LEARNING IMPLEMENTED: store the spells you can cast and pick the one that gives you the most of an ingredient
    if can_brew(best_potion, inv) == False: # check if need to cast a spell
    
    # SORTING WEIGHTED LIST BLOCK       
        # Write code that loops over the potions in the brew, then loops over the spells finding the best spell to cast
        interest = [0.7, 2, 3.3, 4.5]
        not_interest = [0.1, 0.2, 0.4, 0.6]
        sorted_spells = []
        
        for spell in cast:
            # get a delta list of how far away each spell is from making the potion, ignoring deltas not in the potion
            weight = 0
            for i in range(4):
                amount = spell[1][i] + potion[1][i] + inv[0][i]
                if potion[1][i] == 0 or amount > 0:
                    weight += amount * not_interest[i]
                else:
                    weight += amount * -interest[i]
            sorted_spells.append((spell, weight))
        # Sort all the potions and spells by weight (lowest weight first)
        sorted_spells.sort(key = lambda x: x[-1])
    # SORTING WEIGHTED LIST BLOCK
        
        rest_it = True
    # CASTING BLOCK
        # go through the weighted list of spells, and looking to cast the most useful one first
        for spell, weight in sorted_spells:
            # if the spell is really good but we cant cast it just rest
            if weight < 1 and not can_cast(spell, inv):
                cast_it = False
                rest_it = True
                break
            # cast the best spell you can
            elif can_cast(spell, inv):
                cast_it = True
                best_spell = spell
                break
    # CASTING BLOCK
    
    # IF LEARNING IMPLEMENTED: Instead of resting look to learn a new skill
    # Special case of full inventory, check if any potions can be brewed, if not learn a spell
    if sum(inv[0]) == 10 and not cast_it and not can_brew(best_potion, inv):        
        best_potion = [0, 0, 0, 0]
        for potion in brew: 
            if potion[-1] > best_potion[-1] and can_brew(potion, inv):
                best_potion = potion
        if best_potion == [0, 0, 0, 0]:
            for spell in learn[::-1]:
                if can_learn(spell, inv):
                    learn_it = True
                    best_learn = spell
    
    if defo_learn_it:
        print(f"LEARN {best_learn[0]}")
    elif cast_it:
        print(f"CAST {best_spell[0]}")
    elif rest_it:
        print("REST")
    elif learn_it:
        print(f"LEARN {best_learn[0]}")
    else:
        brewed += 1
        print(f"BREW {best_potion[0]}")
    # in the first league: BREW <id> | WAIT; later: BREW <id> | CAST <id> [<times>] | LEARN <id> | REST | WAIT