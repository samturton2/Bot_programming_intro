import sys
import math
import datetime

# define the number of round and number of brewed
brewed = 0
enemy_brewed = [0, 0]
round_i = 0

best_potion = 'nothing' # define best potion, that only gets changed if the potion isnt brewed anymore

# define a function that checks if the spell can be cast
def can_cast(spell_list, inv_list):
    if sum(inv_list[0]) + sum(spell_list[1]) > 10: # checks if inv full
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
    if spell_list[-1] > inv_list[0][0]: # + spell_list[-2]:
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
    t1 = datetime.datetime.now()
    
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
            brew.sort(key = lambda x: x[-1])
        elif action_type == "CAST":
            cast.append([action_id, [delta_0, delta_1, delta_2, delta_3], 1, repeatable, castable])
            if repeatable: # if repeatable also append an instance where its cast twice
                cast.append([action_id, [delta_0*2, delta_1*2, delta_2*2, delta_3*2], 2, repeatable, castable])
        elif action_type == "LEARN":
            learn.append([action_id, [delta_0, delta_1, delta_2, delta_3], 1, repeatable, tax_count, tome_index])
            if repeatable: # if repeatable also append an instance where its would be cast twice
                learn.append([action_id, [delta_0*2, delta_1*2, delta_2*2, delta_3*2], 2, tax_count, tome_index])

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
    deffo_brew_it = False # Assume to not brew
    rest_it = False # Assume to not rest
    deffo_rest_it = False
    cast_it = False # Assume to not cast spell
    learn_it = False # Assume to not learn spell
    deffo_learn_it = False


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
            weighted.append(1001)
        else:
            weighted.append(potion[-1]/weight) # price / difficulty to make 
    print(f"debug ... {max(weighted)}", file=sys.stderr, flush=True)
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
            if option[0][-1] > rup[1]+2-rup[0]: # if the options price overtakes
                if option[1] < min_weight:
                    min_weight = option[1]
                    best_potion = option[0]
        # if best potion still not found pick the one with the highest score

    
    # IF LEARNING IMPLEMENTED: store the spells you can cast and pick the one that gives you the most of an ingredient
    if can_brew(best_potion, inv) == False: # check if need to cast a spell
    
    # SORTING WEIGHTED LIST BLOCK       
        # Write code that loops over the potions in the brew, then loops over the spells finding the best spell to cast
        interest = [0.5, 2, 3.2, 4.5]
        not_interest = [0.1, 0.3, 0.6, 0.9]
        sorted_spells = []
        
        for spell in cast:
            # get a delta list of how far away each spell is from making the potion, ignoring deltas not in the potion
            weight = 0
            for i in range(4):
                amount = spell[1][i] + best_potion[1][i] + inv[0][i]
                if best_potion[1][i] == 0:
                    weight += amount * not_interest[i]
                elif amount >= 0:
                    weight += interest[i]
                else:
                    weight += -interest[i] / amount
            sorted_spells.append((spell, weight))
        # Sort all the spells by weight (lowest weight first)
        sorted_spells.sort(key = lambda x: x[-1])
    # SORTING WEIGHTED LIST BLOCK
        print(f"{sorted_spells[0][1]}", file=sys.stderr, flush=True)
        
    # CASTING BLOCK
      # casts spells to make the chosen potion
        # rest if we cant cast a spell
        rest_it = True
    
        # go through the weighted list of spells, and looking to cast the most useful one first
        for spell, weight in sorted_spells:
            # if the spell is really good but we cant cast it just rest
            if weight > 20 and not spell[-1]:
                break
            # cast the best spell you can
            elif can_cast(spell, inv) and spell[-1]:
                cast_it = True
                best_spell = spell
                special_iter = 0
                break
    # CASTING BLOCK
    
    # Special case of full inventory, check if any potions can be brewed, if not learn a spell
    if sum(inv[0]) >= 9 and not cast_it:
        special_iter += 1
        # if been is special iter for too long cast any spell that makes inventory space
        if special_iter > 2:
            for spell in cast:
                if sum(spell[1])+sum(inv[0]) < sum(inv[0]) and can_cast(spell, inv) and spell[-1]: # if frees up space cast it
                    best_spell = spell
                    cast_it = True
                    break
            if not cast_it:
                for spell in cast: # if not just cast any spell 
                    if can_cast(spell, inv) and spell[-1]: # if can cast it, cast it, unless it gives too many greens
                        if spell[1][1] + inv[0][1] > 6:
                            continue
                        else:
                            best_spell = spell
                            cast_it = True
                            break
        # print(f"debug ... {cast_it}", file=sys.stderr, flush=True)
        if not cast_it:
            if inv[0][0] > 3: # if lots of blues
                for spell in learn[:4]: # learn as high up spell you can learn
                    if can_learn(spell, inv):
                        learn_it = True
                        best_learn = spell
            else:
                for spell in learn[::-1]: # if not just learn a spell
                    if can_learn(spell, inv):
                        learn_it = True
                        best_learn = spell
    
    # print(f"debug ... {best_potion}", file=sys.stderr, flush=True)
    # Find a spell to deffo cast
    if not can_brew(best_potion, inv):
        for potion in brew[::-1]:
            for spell in cast:
                deffo_cast_it = True # Assume to deffo cast it
                if not can_cast(spell, inv) or not spell[-1]:
                    deffo_cast_it = False
                    continue
                for i in range(4):
                    if potion[1][i] + spell[1][i] + inv[0][i] < 0:
                        deffo_cast_it = False
                        break
                if deffo_cast_it and can_cast(spell, inv) and spell[-1]:
                    best_spell = spell
                    special_iter = 0
                    break
            if deffo_cast_it and can_cast(spell, inv) and spell[-1]:
                break

    # Find a spell to deffo learn
    if not can_brew(best_potion, inv) and not deffo_cast_it:
        for potion in brew[::-1]:
            # print(f"{spell[-2]}", file=sys.stderr, flush=True)
            for spell in learn:
                deffo_learn_it = True
                newinv = inv
                newinv[0][0] = inv[0][0]-spell[-1]+spell[-2] # Define inventory of next go if learn spell
                if sum(newinv[0]) > 10: # checks for situation of not collecting all the tax
                    for i in range(1,spell[-2]+1):
                        newinv[0][0] -= i
                        if sum(newinv[0]) <= 10:
                            break

                if not can_learn(spell, inv) or not can_cast(spell, newinv): # if you cant learn the spell or you wouldnt be able to cast it once learnt
                    deffo_learn_it = False
                    continue
                for i in range(4): # check if the spell wouldnt make enough ingredients for potion
                    if potion[1][i] + spell[1][i] + newinv[0][i] < 0 :
                        deffo_learn_it = False
                        break
                if deffo_learn_it and can_learn(spell, inv):
                    best_learn = (spell, potion[-1])
                    break
            if deffo_learn_it and can_learn(spell, inv):
                break

    # Find a time to deffo rest
    if not can_brew(best_potion, inv) and not deffo_cast_it:
        for potion in brew[::-1]:
            for spell in cast:
                if spell[-1] == 0 and can_cast(spell, inv):
                    deffo_rest_it = True # Assume to deffo rest it
                    for i in range(4):
                        if potion[1][i] + spell[1][i] + inv[0][i] < 0:
                            deffo_rest_it = False
                            break
                    if deffo_rest_it and can_cast(spell, inv) and not spell[-1]:
                        best_spell = (spell, potion[-1])
                        break
            if deffo_rest_it:
                break

    # check if both deffo rest it and deffo learn it and find which one gets the higher priced potion
    if deffo_rest_it and deffo_learn_it:
        if best_learn[-1] < best_spell[-1]:
            deffo_learn_it = False
        else:
            deffo_rest_it = False

    # Find a potion to deffo brew
    for potion in brew:
        if can_brew(potion, inv):
            best_potion = potion
            deffo_brew_it = True
  

    t2 = datetime.datetime.now()
    print(f"{t2-t1}", file=sys.stderr, flush=True)
    
    if deffo_brew_it:
        brewed += 1
        print(f"BREW {best_potion[0]}")
    elif deffo_cast_it:
        print(f"CAST {best_spell[0]} {best_spell[2]}")
    elif deffo_rest_it:
        print("REST")
    elif deffo_learn_it:
        print(f"LEARN {best_learn[0][0]}")
    elif learn_it:
        print(f"LEARN {best_learn[0]}")
    elif cast_it:
        print(f"CAST {best_spell[0]} {best_spell[2]}")
    elif rest_it:
        print("REST")
    else:
        brewed += 1
        print(f"BREW {best_potion[0]}")
    # in the first league: BREW <id> | WAIT; later: BREW <id> | CAST <id> [<times>] | LEARN <id> | REST | WAIT