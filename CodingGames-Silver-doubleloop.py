import sys
import math
from datetime import datetime
import copy

# Define the number of round and number of brewed
brewed = 0
enemy_brewed = [0, 0]
round_i = 0

best_potion = 'nothing' # define best potion, that only gets changed if the potion isnt brewed anymore

# Define a function that checks if the spell can be cast (assuming castable)
def can_cast(spell_delta, inv_delta):
    if sum(inv_delta) + sum(spell_delta) > 10: # checks if inv full
        return False
    # check if the inv has the ingredients to cast the spell
    for i in range(4):
        if spell_delta[i] + inv_delta[i] < 0:
            return False
    return True

# Define a function that checks if the potion can be brewed
def can_brew(potion_delta, inv_delta):
    # check if inv has the ingredients to brew the potion
    for i in range(4):
        if potion_delta[i] + inv_delta[i] < 0:
            return False
    return True


# Define a function that give your inventory on the next having learnt a spell
def post_learn_inv(spell_list, inv_list):
    newinv = copy.deepcopy(inv_list)
    newinv[0][0] += -spell_list[-1] + spell_list[-2] # Define inventory of next go if learn spell
    if sum(newinv[0]) > 10: # checks for situation of not collecting all the tax
        for i in range(1, spell_list[-2]+1):
            newinv[0][i] -= i
            if sum(newinv[0]) <= 10:
                return newinv
    else:
        return newinv

# Define a function that gives your inventory on the next having learnt a spell
def post_cast_inv(spell_list, inv_list):
    newinv = copy.deepcopy(inv_list)
    for i in range(4):
        newinv[0][i] += spell_list[1][i]
    return newinv

# Define a function to check if a potion is in the list of potions
def in_brew(a_potion, brew_list):
    for i in range(len(brew_list)):
        if a_potion[0] == brew_list[i][0]:
            return True
    return False


# Define a function that checks if you can deffo brew a potion
def deffo_brew(brew_list, inv_list):
    for potion in brew_list[::-1]:
        if can_brew(potion[1], inv_list[0]):
            return (True, potion, potion[-1])
    return (False, 0, 0)

# # Define a function that checks if an uncastable spell would get you a potion
# def deffo_rest(cast_list, brew_list, inv_list):
#     for potion in brew_list[::-1]: # prioritise higher price potions
#         for spell in cast_list:
#             if not spell[-1] and can_cast(spell[1], inv[0]): # if not castable but you could cast it
#                 deffo_rest_it = True
#                 for i in range(4):
#                     if spell[1][i] + inv[0][i] + potion[0][i] < 0:
#                         deffo_rest_it = False
#                         break
#                 if deffo_rest_it:
#                     return (True, spell, potion[-1])
#     return (False, 0, 0)

# Define a function that checks if you are one cast away (Iteration of just check if we should rest this to cast it)
def deffo_cast(cast_list, brew_list, inv_list):
    for potion in brew_list[::-1]:
        for spell in cast_list:
            if can_cast(spell[1], inv_list[0]):
                deffo_cast_it = True
                for i in range(4):
                    if spell[1][i] + inv_list[0][i] + potion[1][i] < 0:
                        deffo_cast_it = False
                        break
                if deffo_cast_it:
                    return (True, spell, potion[-1])
    return (False, 0, 0)

# Define a function that check if you should definately learn a spell
def deffo_learn(learn_list, brew_list, inv_list):
    for potion in brew_list[::-1]:
        for spell in learn_list:
            if spell[-1] <= inv_list[0][0]: # if i can learn it
                newinv = post_learn_inv(spell, inv_list)[:]
                if can_cast(spell[1], newinv[0]): # if i could cast it
                    deffo_learn_it = True
                    for i in range(4):
                        if potion[1][i] + spell[1][i] + newinv[0][i] < 0:
                            deffo_learn_it = False
                            break
                    if deffo_learn_it:
                        return (True, spell, potion[-1])
    return (False, 0, 0)

# Define a function that casts a spell, and returns the newinventory
def second_last_cast(cast_list, brew_list, inv_list):
    for spell in cast_list:
        if can_cast(spell[1], inv_list[0]):
            newinv = post_cast_inv(spell, inv_list)[:]
            if deffo_cast(cast_list, brew_list, newinv)[0]: # iteration depending on time: or deffo_learn()[0] or deffo_rest()[0]
                return (True, spell)
    return (False, 0)


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
# game loop
while True:
    t1 = datetime.now()
    
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
            cast.append([action_id, [delta_0, delta_1, delta_2, delta_3], 1, repeatable, castable])
            if repeatable: # if repeatable also append an instance where its cast twice
                cast.append([action_id, [delta_0*2, delta_1*2, delta_2*2, delta_3*2], 2, repeatable, castable])
        elif action_type == "LEARN":
            learn.append([action_id, [delta_0, delta_1, delta_2, delta_3], 1, repeatable, tax_count, tome_index])
            if repeatable: # if repeatable also append an instance where its would be cast twice
                learn.append([action_id, [delta_0*2, delta_1*2, delta_2*2, delta_3*2], 2, tax_count, tome_index])

    # sort brew list by price (small to large)
    brew.sort(key = lambda x: x[-1])
    # sort spell by sum of delta (small to large)
    cast.sort(key = lambda x: sum(x[1]))

    for i in range(2):
        # inv_0: tier-0 ingredients in inventory
        # score: amount of rupees
        inv_0, inv_1, inv_2, inv_3, score = [int(j) for j in input().split()]
        # load in mine and enemies inventory
        inv.append([inv_0, inv_1, inv_2, inv_3])
        rup.append(score)
    
    # Write an action using print
    # to debug: print("Debug messages...", file=sys.stderr, flush=True)

# OPPONENT BREW COUNT
    if rup[1] > enemy_brewed[1]:
        enemy_brewed[0] += 1
        enemy_brewed[1] = rup[1]
    
    deffo_rest_it = False
    cast_it = False # Assume to not cast spell
    learn_it = False # Assume to not learn spell


# FIND A POTION TO DEFINATELY BREW
    deffo_brew_it, deffo_brew_potion, deffo_brew_potion_price = deffo_brew(brew, inv)

# FIND A POTION TO DEFINATELY CAST
    if not deffo_brew_it:
        deffo_cast_it, deffo_cast_spell, deffo_cast_potion_price = deffo_cast(cast, brew, inv)
        if deffo_cast_it:
# IF NOT CASTABLE, LOOK TO REST TO CAST THE SPELL
            if not deffo_cast_spell[-1]:
                deffo_cast_it = False
                deffo_rest_it = True
# LOOK FOR SPELL TO DEFFO LEARN  # Iteration, and compare to rest it spell
        else:
            deffo_learn_it, deffo_learn_spell, deffo_learn_potion_price = deffo_learn(cast, brew, inv)
            if not deffo_learn_it:
# LOOK FOR SECOND SPELL TO CAST
                second_last_cast_it, second_last_spell = second_last_cast(cast, brew, inv)
                # print(f"{inv[0]}", file=sys.stderr, flush=True)
                if second_last_cast_it:
                    if not second_last_spell[-1]:
                        second_last_cast_it = False
                        deffo_rest_it = True
                else:
# LEARN 5 POTIONS AT THE START
                    if round_i in range(7):
                        best_learn = learn[0]
                        learn_it = True
# FIND THE BEST POTION TO LEARN
                    else:
                        diff_index = [0.1, 0.8, 1.8, 2.8]
                        max_ratio = 0 # make a list to score the potions on the ratio of how many rupies they give you : how hard they are to make with ingredients you have (higher the score the better)
                        for potion in brew[::-1]:
                            weight = 0
                            for i in range(4):
                                if inv[0][i] < -potion[1][i]: # Check if we don't have enough ingredients, if enough difficulty to make is 0 so we pass
                                    weight += -(potion[1][i] + inv[0][i]) * diff_index[i] # negative number takes into account negative potion deltas
                            if potion[-1]/weight > max_ratio:
                                max_ratio = potion[-1]
                                best_potion = potion

                        for option in weighted:
                            if option[0][-1] > rup[1]+2-rup[0]: # if the options price overtakes
                                if option[1] < min_weight:
                                     min_weight = option[1]
                                     best_potion = option[0]
    # FIND THE BEST SPELL TO CAST
            # IF LESS THAN 4 INGREDIENTS CAST A SPELL THAT GETS YOU MORE
                        if sum(inv[0]) < 4:
                            for spell in cast:
                                if can_cast(spell[1], inv[0]) and spell[-1]:
                                    cast_it = True
                                    best_spell = spell
                                    break
            # TRY AND BREW POTIONS LEADING TOWARDS THE BEST POTION
                        if not cast_it:
                    # SORTING WEIGHTED SPELL BLOCK       
                            # Write code that loops over the potions in the brew, then loops over the spells finding the best spell to cast
                            interest = [0.7, 2, 3.3, 4.5]
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
                            # Sort all the potions and spells by weight (lowest weight first)
                            sorted_spells.sort(key = lambda x: x[-1])
                    # TRYING TO WORK TOWARDS A POTION TO BREW
                            # check what ingredient i need more of
                                                                # for i in range(4):
                                                                #     if best_potion[1][i] + inv[0][i] < 0:
                                                                #         need_more = i
                                                                # # loop round ingredients, updating the need_more to a less expensive ingredient
                                                                # for _ in range(need_more, -1, -1):
                                                                #     # check spells if they can provide me with more of that
                                                                #     for spell, weight in sorted_spells:
                                                                #         if spell[1][_] > 0 and can_cast(spell[1], inv[0]) and spell[-1]:
                                                                #             # if we cast a spell we break the loops and do it
                                                                #             cast_it = True
                                                                #             best_spell = spell
                                                                #             break
                                                                #     if cast_it:
                                                                #         special_iter = 0 # reset special iter
                                                                #         break
                            rest_it = True

                            # go through the weighted list of spells, and looking to cast the most useful one first
                            for spell, weight in sorted_spells:
                                # if the spell is really good but we cant cast it just rest
                                if weight > 20 and can_cast(spell[1], inv[0]) and not spell[-1]:
                                    break
                                # cast the best spell you can
                                elif can_cast(spell[1], inv[0]) and spell[-1]:
                                    cast_it = True
                                    best_spell = spell
                                    special_iter = 0
                                    break
            # SPECIAL CASE OF FULL INVENTORY
                        if sum(inv[0]) >= 9 and not cast_it:
                            special_iter += 1
                            # if been is special iter for too long cast any spell that makes inventory space
                            if special_iter > 2:
                                for spell in cast:
                                    if sum(spell[1]) < 0 and can_cast(spell[1], inv[0]) and spell[-1]: # if frees up space cast it
                                        best_spell = spell
                                        cast_it = True
                                        break
                                if not cast_it:
                                    for spell in cast: # if not just cast any spell 
                                        if can_cast(spell[1], inv[0]) and spell[-1]: # if can cast it, cast it, unless it gives too many greens
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
                                        if spell[-1] <= inv[0][0]:
                                            learn_it = True
                                            best_learn = spell
                                else:
                                    for spell in learn[::-1]: # if not just learn a spell
                                        if spell[-1] <= inv[0][0]:
                                            learn_it = True
                                            best_learn = spell













# TIMEING THE CODE
    t2 = datetime.now()
    print(f"{t2-t1}", file=sys.stderr, flush=True)
    

# FINAL OUTPUTS    
    if deffo_brew_it:
        brewed += 1
        print(f"BREW {deffo_brew_potion[0]}")
    elif deffo_cast_it:
        print(f"CAST {deffo_cast_spell[0]} {deffo_cast_spell[2]}")
    elif deffo_rest_it:
        print("REST")
    elif deffo_learn_it:
        print(f"LEARN {deffo_learn_spell[0][0]}")
    elif second_last_cast_it:
        print(f"CAST {second_last_spell[0]} {second_last_spell[2]}")
    elif cast_it:
        print(f"CAST {best_spell[0]} {best_spell[2]}")
    elif learn_it:
        print(f"LEARN {best_learn[0]}")
    else:
        print("REST")
    # in the first league: BREW <id> | WAIT; later: BREW <id> | CAST <id> [<times>] | LEARN <id> | REST | WAIT