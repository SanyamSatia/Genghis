import riskengine
import riskgui
import random
import math
from aihelper import *
from turbohelper import *
from risktools import *

#This is the function implement to implement an AI.  Then this ai will work with either the gui or the play_risk_ai script
def getAction(state, time_left=None):
    """This is the main AI function.  It should return a valid AI action for this state."""
    #Get the possible actions in this state
    actions = getAllowedActions(state)
    myaction = random.choice(actions)

    # edited by sarah
    max_sum=0
    if state.turn_type == 'Attack':
        bestp=0.0
        besth=0.0
        bestf=0.0
        for a in actions:
            if a.to_territory is not None:
                curh =  heuristic(state, state.board.territory_to_id[a.to_territory])
                opparmy = state.armies[state.board.territory_to_id[a.to_territory]]
                homarmy = state.armies[state.board.territory_to_id[a.from_territory]]
                curprob = compute_probability(homarmy,opparmy)
                fcost=curprob+curh

                if(fcost > bestf):
                    bestf = fcost
                    bestp=curprob
                    myaction=a

                '''
                successor_states, successor_probs = simulateAttack(state,a)
                if successor_probs[0] == 1:
                    print('card logic')
                p=0
                for s in successor_states:
                    if s.owners[state.board.territory_to_id[a.to_territory]] == state.current_player:
                        sum = 4*armydiff + successor_probs[p] + frndneigh
                        if sum > max_sum:
                            max_sum = sum
                            myaction = a
                    p=p+1
                '''
        #best attack probability found through experimentation
        if(bestp<0.76):
            myaction=actions[-1]
    #edited upto this

    #pass troops from any territory not facing enemies to a neighboring territory facing an enemy
    if state.turn_type == 'Fortify':
        for a in actions:
            if a.from_territory == None or a.to_territory == None:
                continue
            fort = 1
            for n in state.board.territories[state.board.territory_to_id[a.from_territory]].neighbors:
                if state.owners[n] != state.current_player:
                    fort = 0
                    break
            #don't move troops if territory facing a neighbor
            if fort == 0:
                continue

            for n in state.board.territories[state.board.territory_to_id[a.to_territory]].neighbors:
                if state.owners[n] != state.current_player:
                    myaction  = a

    if state.turn_type == 'PreAssign':

        possible_actions = []
        territories =['Eastern Australia', 'Western Australia', 'Colombia', 'Chile', 'Peru', 'Brazil', 'Indonesia', 'New Guinea']
        for a in actions:
            #if the territories above are not occupied, try to occupy it
            if a.to_territory in territories:
                #s = a.print_action()
                return a
            else:
                #number_of_fronts = len(state.board.territories[state.board.territory_to_id[a.to_territory]].neighbors)
                if TFrontsCount(state.board.territories[state.board.territory_to_id[a.to_territory]], None) <4:
                    possible_actions.append(a)

        if len(possible_actions) > 0:
            myaction = random.choice(possible_actions)
        else:
            myaction = random.choice(actions)

    if state.turn_type == 'PrePlace':
        possible_actions = []
        bordering_armies = 0
        for a in actions:
            #check to see how many tiles are bordering with the enemies
            if TFrontsCount(state.board.territories[state.board.territory_to_id[a.to_territory]], None) >0:
                for n in state.board.territories[state.board.territory_to_id[a.to_territory]].neighbors:
                    if state.owners[n] != state.current_player:
                        bordering_armies += state.armies[n]
                if bordering_armies > state.armies[state.board.territory_to_id[a.to_territory]]:
                    possible_actions.append(a)
        if len(possible_actions) > 0:
            myaction = random.choice(possible_actions)

    if state.turn_type == 'Place':
        min_enem_neigh=100
        for a in actions:
            if a.to_territory is not None:
                enem_neigh=0
                for n in state.board.territories[state.board.territory_to_id[a.to_territory]].neighbors:
                    if state.owners[n] != state.current_player:
                        enem_neigh += 1
                        #check troops difference between enemy neighbour and mine
                        my_troops = state.armies[state.board.territory_to_id[a.to_territory]]
                        neigh_troops = state.armies[n]
                        if my_troops > (neigh_troops*3):
                            enem_neigh=0
                            break
                if(enem_neigh>0 and enem_neigh < min_enem_neigh):
                    min_enem_neigh = enem_neigh
                    myaction = a
        if min_enem_neigh == 100:
            #print "random place action"
            myaction = random.choice(actions)

    return myaction
#return the continent of the given territory.
def toContinent(state, territory):
     for c in state.board.continents.itervalues():
        if territory in c.territories:
            #print "territoriesOwned: ", territoriesOwned(state, c)
            return c
#calculate the percentage of owned territories in the continent, assuming if he can take this territories.
def continentProgress (state, continent):
    terrOwned = 0.0
    terrContinent = 0.0
    for territories in continent.territories:
        terrContinent +=1.0
        if state.owners[territories] == state.current_player:
            terrOwned += 1.0
    return (terrOwned+1.0)/terrContinent

def heuristic(state, territory):
    heuristic = 0
    continent = toContinent(state, territory)
    progress = continentProgress(state, continent)
    heuristic = 10.0 * progress
    if progress ==1:
        heuristic += 10
    continentName = continent.name
    if continentName == "N. America":
        heuristic += 5
    elif continentName == "S. America":
        heuristic += 4
    elif continentName =="Australia":
        heuristic += 3
    elif continentName == "Europe":
        heuristic += 1
    elif continentName == "Africa":
        heuristic += 2
    return (heuristic/2500)

def compute_probability(homarmy, opparmy):
    prob=0.0
    if(homarmy>=3 and opparmy>=2):
        homarmy=homarmy*1.15
    prob=homarmy/opparmy
    prob*=0.4
    return prob

#Stuff below this is just to interface with Risk.pyw GUI version
#DO NOT MODIFY

def aiWrapper(function_name, occupying=None):
    game_board = createRiskBoard()
    game_state = createRiskState(game_board, function_name, occupying)
    action = getAction(game_state)
    return translateAction(game_state, action)

def Assignment(player):
#Need to Return the name of the chosen territory
    return aiWrapper('Assignment')

def Placement(player):
#Need to return the name of the chosen territory
     return aiWrapper('Placement')


def Attack(player):
 #Need to return the name of the attacking territory, then the name of the defender territory
    return aiWrapper('Attack')


def Occupation(player,t1,t2):
 #Need to return the number of armies moving into new territory
    occupying = [t1.name,t2.name]
    aiWrapper('Occupation',occupying)

def Fortification(player):
    return aiWrapper('Fortification')
