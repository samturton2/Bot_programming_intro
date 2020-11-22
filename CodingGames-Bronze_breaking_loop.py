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


    # on the first 5 turns learn a spell
    if round_i in range(5):
        for spell in learn[::-1]:
            if can_learn(spell, inv):
                learn_it = True
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
            if inv[0][i] < -potion[1][i]: # Check if we have we don't have enough ingredients, if enough difficulty to make is 0 so we pass
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
    
        # WRITE CODE WHICH SCORES THE SPELLS IN TERMS OF USEFULLNESS
        difficulty = [0.8, 1.3, 1.8, 2.3]
        weighted_cast = []
        sorted_cast = []
        for spell in cast:
            weight = 0
            for i in range(4): # Find how many ingredients away from the best_potion the spell gets
                if best_potion[1][i] + inv[0][i] + spell[1][i] < 0:
                    weight += ((best_potion[1][i] + inv[0][i] + spell[1][i]) * -difficulty[i])

            weighted_cast.append([spell, weight])
            
        # order the list by weight, having smallest weight first
        weighted_cast.sort(key = lambda x: x[1])
        # load into sorted_cast
        for spell in weighted_cast:
            sorted_cast.append(spell[0])
        # print(f"debug ... {weighted_cast}", file=sys.stderr, flush=True) 
    
    # casts spells to make the chosen potion
        # rest if we cant cast a spell
        rest_it = True
        # check what ingredient i need more of
        for i in range(4):
            if best_potion[1][i] + inv[0][i] < 0:
                need_more = i
        # loop round ingredients, updating the need_more to a less expensive ingredient
        for _ in range(need_more, -1, -1):
            # check spells if they can provide me with more of that
            for spell in sorted_cast:# cast[::-1]:
                if spell[1][_] > 0 and can_cast(spell, inv):
                    # if we cast a spell we break the loops and do it
                    cast_it = True
                    best_spell = spell
                    break
            if cast_it:
                special_iter = 0 #reset special iter
                break
    
    # IF LEARNING IMPLEMENTED: Instead of resting look to learn a new skill
    # Special case of full inventory, check if any potions can be brewed, if not learn a spell
    if sum(inv[0]) >= 9 and not cast_it and not can_brew(best_potion, inv):
        special_iter += 1
        best_potion = [0, 0, 0, 0]
        for potion in brew: 
            if potion[-1] > best_potion[-1] and can_brew(potion, inv):
                best_potion = potion
        # if been is special iter for too long cast any spell that makes inventory space
        if special_iter > 2 and not can_brew(potion, inv):
            for spell in cast:
                if sum(spell[1])+sum(inv[0]) < 10 and can_cast(spell, inv): # if frees up space cast it
                    best_spell = spell
                    cast_it = True
                    break
            if not cast_it:
                for spell in cast:
                    if can_cast(spell, inv): # if can cast, cast it
                        best_spell = spell
                        cast_it = True
                        break

        if best_potion == [0, 0, 0, 0] and not cast_it:
            for spell in learn[::-1]:
                if can_learn(spell, inv):
                    learn_it = True
                    best_learn = spell
    
    if learn_it:
        print(f"LEARN {best_learn[0]}")
    elif cast_it:
        print(f"CAST {best_spell[0]}")
    elif rest_it:
        print("REST")
    else:
        brewed += 1
        print(f"BREW {best_potion[0]}")
    # in the first league: BREW <id> | WAIT; later: BREW <id> | CAST <id> [<times>] | LEARN <id> | REST | WAIT