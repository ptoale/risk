#!/usr/bin/env python

"""
Risk

This module provides methods for calculating odds of an attacking player to win
a territory in the game of Risk. 

1) The game is determined by a large number of battles between adjoining 
territories. A player, on his/her turn, can attack from any friendly territory 
with at least 2 troops, to any neighboring enemy territory. 
    - The reason that the attacker must have at least 2 troops is that no 
    territory can be left defenseless. 
    - This also means that the maximum size of an attacking army is one less 
    than the number of troops in the attacking territory.
    - In the code below, the number of attacking troops is always the number of 
    troops actually attacking.

2) The attacking player may roll one die, up to a maximum of 3, for each 
attacking troop. The defending player may roll one die, up to a maximum of 2, 
for each defending troop. The dice are ordered from highest to lowest and 
compared pairwise: highest attacking die vs highest defending die, next-highest 
attacking die vs next-highest defending die, etc. The higher die in the pair 
wins, with ties going to the defender.
    - Because the defender has at most 2 die, each roll will compare either 1 
    or 2 pairs of dice.
    - This means that there are 6 possible rolls: 3-2, 3-1, 2-2, 2-1, 1-2, 
    and 1-1.
    - If both players roll at least 2 die (3-2, 2-2), 2 troops will die.
    - Otherwise (3-1, 2-1, 1-2, 1,1), only 1 troop will die.
    
3) A territory is won when the last defending troop dies. If all of the 
attacking troops die before this happens, the attack is over and the defender
maintains control.

"""

"""
The following 6 methods count the possible outcomes of the 6 different rolls.
They do so by enumerating all possible results of the roll and summing the 
number in which the attacker losses none, the attacker losses 1, and when 
appropriate, the attacker losses 2.
"""

import random

MAX_TROOP_CACHE = 100
CACHE_SIZE = MAX_TROOP_CACHE*MAX_TROOP_CACHE
CACHE = [None]*CACHE_SIZE

def cache_index(n_attack, n_defend):
    return (n_defend-1)*MAX_TROOP_CACHE + (n_attack-1)

def roll32(verbose=False):
    """
    For 3 attacking 2, 2 troops will die. The possible outcomes are:
        - defender looses 2
        - attacker and defender both loss 1
        - attacker looses 2
    The function calculates each probability and returns them as a list, ordered as
    described here.

    """

    n_combos = 0
    n_a_wins_2 = 0
    n_a_wins_1 = 0
    n_a_wins_0 = 0

    # Iterate over the 3 attacking dice
    for a1 in range(1, 7):
        for a2 in range(1, 7):
            for a3 in range(1, 7):
            
                # Sort the attacking roll from highest to lowest
                a_roll = sorted([a1, a2, a3], reverse=True)
            
                # Iterate over the 2 defending dice
                for d1 in range(1, 7):
                    for d2 in range(1, 7):
                    
                        # Sort the defending roll from highest to lowest
                        d_roll = sorted([d1, d2], reverse=True)
                        
                        # Count this combo
                        n_combos += 1

                        # Compare the dice pairwise                            
                        if a_roll[0] > d_roll[0]:
                            if a_roll[1] > d_roll[1]:
                                n_a_wins_2 += 1
                            else:
                                n_a_wins_1 += 1
                        else:
                            if a_roll[1] > d_roll[1]:
                                n_a_wins_1 += 1
                            else:
                                n_a_wins_0 += 1

    # These are the probabilities, named by the number of lost attacking troops
    p32_0 = (1.*n_a_wins_2)/n_combos
    p32_1 = (1.*n_a_wins_1)/n_combos
    p32_2 = (1.*n_a_wins_0)/n_combos

    if verbose:
        print "Probabilities for 3 attacking 2:"
        print "  Attacker looses 0: (%d/%d) = %f" % (n_a_wins_2, n_combos, p32_0)
        print "  Attacker looses 1: (%d/%d) = %f" % (n_a_wins_1, n_combos, p32_1)
        print "  Attacker looses 2: (%d/%d) = %f" % (n_a_wins_0, n_combos, p32_2)

    return p32_0, p32_1, p32_2


def roll22(verbose=False):
    """
    For 2 attacking 2, 2 troops will die. The possible outcomes are:
        - defender looses 2
        - attacker and defender both loss 1
        - attacker looses 2
    The function calculates each probability and returns them as a list, ordered as
    described here.

    """

    n_combos = 0
    n_a_wins_2 = 0
    n_a_wins_1 = 0
    n_a_wins_0 = 0

    # Iterate over the 2 attacking dice
    for a1 in range(1, 7):
        for a2 in range(1, 7):
            
            # Sort the attacking roll from highest to lowest
            a_roll = sorted([a1, a2], reverse=True)
            
            # Iterate over the 2 defending dice
            for d1 in range(1, 7):
                for d2 in range(1, 7):
                    
                    # Sort the defending roll from highest to lowest
                    d_roll = sorted([d1, d2], reverse=True)
                        
                    # Count this combo
                    n_combos += 1

                    # Compare the dice pairwise                            
                    if a_roll[0] > d_roll[0]:
                        if a_roll[1] > d_roll[1]:
                            n_a_wins_2 += 1
                        else:
                            n_a_wins_1 += 1
                    else:
                        if a_roll[1] > d_roll[1]:
                            n_a_wins_1 += 1
                        else:
                            n_a_wins_0 += 1

    # These are the probabilities, named by the number of lost attacking troops
    p22_0 = (1.*n_a_wins_2)/n_combos
    p22_1 = (1.*n_a_wins_1)/n_combos
    p22_2 = (1.*n_a_wins_0)/n_combos

    if verbose:
        print "Probabilities for 2 attacking 2:"
        print "  Attacker looses 0: (%d/%d) = %f" % (n_a_wins_2, n_combos, p22_0)
        print "  Attacker looses 1: (%d/%d) = %f" % (n_a_wins_1, n_combos, p22_1)
        print "  Attacker looses 2: (%d/%d) = %f" % (n_a_wins_0, n_combos, p22_2)

    return p22_0, p22_1, p22_2


def roll31(verbose=False):
    """
    For 3 attacking 1, 1 troop will die. The possible outcomes are:
        - defender looses 1
        - attacker looses 1
    The function calculates each probability and returns them as a list, ordered as
    described here.

    """

    n_combos = 0
    n_a_wins_1 = 0
    n_a_wins_0 = 0

    # Iterate over the 3 attacking dice
    for a1 in range(1, 7):
        for a2 in range(1, 7):
            for a3 in range(1, 7):
            
                # Sort the attacking roll from highest to lowest
                a_roll = sorted([a1, a2, a3], reverse=True)
            
                # Iterate over the 1 defending die
                for d1 in range(1, 7):
                    
                    # Sort the defending roll from highest to lowest
                    d_roll = sorted([d1], reverse=True)
                        
                    # Count this combo
                    n_combos += 1

                    # Compare the dice pairwise                            
                    if a_roll[0] > d_roll[0]:
                        n_a_wins_1 += 1
                    else:
                        n_a_wins_0 += 1

    # These are the probabilities, named by the number of lost attacking troops
    p31_0 = (1.*n_a_wins_1)/n_combos
    p31_1 = (1.*n_a_wins_0)/n_combos

    if verbose:
        print "Probabilities for 3 attacking 1:"
        print "  Attacker looses 0: (%d/%d) = %f" % (n_a_wins_1, n_combos, p31_0)
        print "  Attacker looses 1: (%d/%d) = %f" % (n_a_wins_0, n_combos, p31_1)

    return p31_0, p31_1


def roll21(verbose=False):
    """
    For 2 attacking 1, 1 troop will die. The possible outcomes are:
        - defender looses 1
        - attacker looses 1
    The function calculates each probability and returns them as a list, ordered as
    described here.

    """

    n_combos = 0
    n_a_wins_1 = 0
    n_a_wins_0 = 0

    # Iterate over the 2 attacking dice
    for a1 in range(1, 7):
        for a2 in range(1, 7):
            
            # Sort the attacking roll from highest to lowest
            a_roll = sorted([a1, a2], reverse=True)
            
            # Iterate over the 1 defending die
            for d1 in range(1, 7):
                    
                # Sort the defending roll from highest to lowest
                d_roll = sorted([d1], reverse=True)
                        
                # Count this combo
                n_combos += 1

                # Compare the dice pairwise                            
                if a_roll[0] > d_roll[0]:
                    n_a_wins_1 += 1
                else:
                    n_a_wins_0 += 1

    # These are the probabilities, named by the number of lost attacking troops
    p21_0 = (1.*n_a_wins_1)/n_combos
    p21_1 = (1.*n_a_wins_0)/n_combos

    if verbose:
        print "Probabilities for 2 attacking 1:"
        print "  Attacker looses 0: (%d/%d) = %f" % (n_a_wins_1, n_combos, p21_0)
        print "  Attacker looses 1: (%d/%d) = %f" % (n_a_wins_0, n_combos, p21_1)

    return p21_0, p21_1


def roll12(verbose=False):
    """
    For 1 attacking 2, 1 troop will die. The possible outcomes are:
        - defender looses 1
        - attacker looses 1
    The function calculates each probability and returns them as a list, ordered as
    described here.

    """

    n_combos = 0
    n_a_wins_1 = 0
    n_a_wins_0 = 0

    # Iterate over the 1 attacking die
    for a1 in range(1, 7):
            
        # Sort the attacking roll from highest to lowest
        a_roll = sorted([a1], reverse=True)
            
        # Iterate over the 2 defending dice
        for d1 in range(1, 7):
            for d2 in range(1, 7):
                    
                # Sort the defending roll from highest to lowest
                d_roll = sorted([d1, d2], reverse=True)
                        
                # Count this combo
                n_combos += 1

                # Compare the dice pairwise                            
                if a_roll[0] > d_roll[0]:
                    n_a_wins_1 += 1
                else:
                    n_a_wins_0 += 1

    # These are the probabilities, named by the number of lost attacking troops
    p12_0 = (1.*n_a_wins_1)/n_combos
    p12_1 = (1.*n_a_wins_0)/n_combos

    if verbose:
        print "Probabilities for 1 attacking 2:"
        print "  Attacker looses 0: (%d/%d) = %f" % (n_a_wins_1, n_combos, p12_0)
        print "  Attacker looses 1: (%d/%d) = %f" % (n_a_wins_0, n_combos, p12_1)

    return p12_0, p12_1


def roll11(verbose=False):
    """
    For 1 attacking 1, 1 troop will die. The possible outcomes are:
        - defender looses 1
        - attacker looses 1
    The function calculates each probability and returns them as a list, ordered as
    described here.

    """

    n_combos = 0
    n_a_wins_1 = 0
    n_a_wins_0 = 0

    # Iterate over the 1 attacking die
    for a1 in range(1, 7):
            
        # Sort the attacking roll from highest to lowest
        a_roll = sorted([a1], reverse=True)
            
        # Iterate over the 1 defending die
        for d1 in range(1, 7):
                    
            # Sort the defending roll from highest to lowest
            d_roll = sorted([d1], reverse=True)
                        
            # Count this combo
            n_combos += 1

            # Compare the dice pairwise                            
            if a_roll[0] > d_roll[0]:
                n_a_wins_1 += 1
            else:
                n_a_wins_0 += 1

    # These are the probabilities, named by the number of lost attacking troops
    p11_0 = (1.*n_a_wins_1)/n_combos
    p11_1 = (1.*n_a_wins_0)/n_combos

    if verbose:
        print "Probabilities for 1 attacking 1:"
        print "  Attacker looses 0: (%d/%d) = %f" % (n_a_wins_1, n_combos, p11_0)
        print "  Attacker looses 1: (%d/%d) = %f" % (n_a_wins_0, n_combos, p11_1)

    return p11_0, p11_1


def prob(n_attack, n_defend, verbose=False):
    """
    This function calculates the probability that a territory is captured by
    an attacking army. It makes use of the calculated probabilities of the 6 
    possible rolls.
    
    """

    # Check for end conditions
    if n_attack == 0:
        return 0.0
    elif n_defend == 0:
        return 1.0
        
    # Split by number of pairs to compare
    #   3-2 2-2
    #   3-1 2-1 1-2 1-1
    if min(n_attack, n_defend) >= 2:
        if n_attack >= 3:
            p0, p1, p2 = roll32(verbose)
        else:
            p0, p1, p2 = roll22(verbose)
        
        i2 = cache_index(n_attack, n_defend-2)
        if CACHE[i2]:
            p_a2 = CACHE[i2]
        else:
            p_a2 = prob(n_attack, n_defend-2, verbose)
            CACHE[i2] = p_a2
            
        i1 = cache_index(n_attack-1, n_defend-1)
        if CACHE[i1]:
            p_a1 = CACHE[i1]
        else:
            p_a1 = prob(n_attack-1, n_defend-1, verbose)
            CACHE[i1] = p_a1
            
        i0 = cache_index(n_attack-2, n_defend)
        if CACHE[i0]:
            p_a0 = CACHE[i0]
        else:
            p_a0 = prob(n_attack-2, n_defend, verbose)
            CACHE[i0] = p_a0
            
        return p0*p_a2 + p1*p_a1 + p2*p_a0

    else:
        if n_attack >= 3:
            p0, p1 = roll31(verbose)
        elif n_attack == 2:
            p0, p1 = roll21(verbose)
        elif n_defend >= 2:
            p0, p1 = roll12(verbose)
        else:
            p0, p1 = roll11(verbose)

        i1 = cache_index(n_attack, n_defend-1)
        if CACHE[i1]:
            p_a1 = CACHE[i1]
        else:
            p_a1 = prob(n_attack, n_defend-1, verbose)
            CACHE[i1] = p_a1
            
        i0 = cache_index(n_attack-1, n_defend)
        if CACHE[i0]:
            p_a0 = CACHE[i0]
        else:
            p_a0 = prob(n_attack-1, n_defend, verbose)
            CACHE[i0] = p_a0
            
        return p0*p_a1 + p1*p_a0


def scan(max_attack, max_defend, verbose=False):

    for a in range(1, max_attack+1):
        for d in range(1, max_defend+1):
            p = prob(a, d, verbose)
            print "Prob(%d, %d) = %e" % (a, d, p)


def battle(n_attack, n_defend, verbose=False, rng=None):
        
    r = rng or random.Random()
        
    while n_attack > 0 and n_defend > 0:

        if verbose:
            print "FIGHT! %d attacking %d" % (n_attack, n_defend)

        a = 3 if n_attack > 3 else n_attack
        d = 2 if n_defend > 2 else n_defend
            
        na, nd = roll(a, d, r, verbose)
        n_attack -= na
        n_defend -= nd
            
    if n_defend == 0:
        if verbose:
            print "Attacker Wins!!!"
        return n_attack
            
    else:
        if verbose:
            print "Defender Wins!!!"
        return 0

def roll(n_attack, n_defend, rng, verbose=False):
        
    attackRoll = sorted([rng.randint(1,6) for i in range(n_attack)], reverse=True)
    defendRoll = sorted([rng.randint(1,6) for i in range(n_defend)], reverse=True)
    
    if verbose:
        print "  Attacker rolls: %s" % attackRoll
        print "  Defender rolls: %s" % defendRoll
    
    dLost = 0
    aLost = 0
                
    for ar, dr in zip(attackRoll, defendRoll):
        loser = 'Attacker'
        if ar > dr:
            loser = 'Defender'
            dLost += 1
        else:
            aLost += 1
                
        if verbose:
            print "  Comparing Attack=%d  Defend=%d  ----> %s losses 1 troop!" % (ar, dr, loser)            

    if verbose:
        print "         Lost Troops: Attacking=%d  Defending=%d" % (aLost, dLost)

    return aLost, dLost


if __name__ == '__main__':

    import sys
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Calculate the probability of winning a territory in RISK.')
    parser.add_argument('attack', metavar='<n_attack>', type=int,
                        help='Number of attacking troops')
    parser.add_argument('defend', metavar='<n_defend>', type=int,
                        help='Number of defending troops')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='print some junk')
    parser.add_argument('-s', '--scan', action='store_true', 
                        help='scan all combinations from (1,1) to (a,d)')
    parser.add_argument('-r', '--roll', action='store_true',
                        help='print the roll data')
    parser.add_argument('-b', '--battle', action='store_true',
                        help='simulate a battle')
    args = parser.parse_args()

    if args.roll:
        roll11(True)
        roll21(True)
        roll31(True)
        roll12(True)
        roll22(True)
        roll32(True)

    if args.battle:
        a = battle(args.attack, args.defend, args.verbose)
        print "Attacker has %d troops remaining" % a
        sys.exit()

    if args.scan:
        scan(args.attack, args.defend, args.verbose)
    else:
        p = prob(args.attack, args.defend, args.verbose)
        print "Prob(%d, %d) = %e" % (args.attack, args.defend, p)
