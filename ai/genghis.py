import riskengine
import riskgui
import random
from aihelper import *
from turbohelper import *
from risktools import *

#This is the function implement to implement an AI.  Then this ai will work with either the gui or the play_risk_ai script
def getAction(state, time_left=None):
    """This is the main AI function.  It should return a valid AI action for this state."""

    #Get the possible actions in this state
    actions = getAllowedActions(state)

    #Select a Random Action
    myaction = random.choice(actions)

    # edited by sarah
    maxdiff = 0;
    if state.turn_type == 'Attack':
        for a in actions:
            if a.to_territory is not None:
                armydiff = state.armies[state.board.territory_to_id[a.from_territory]] - state.armies[state.board.territory_to_id[a.to_territory]]
                if(armydiff > maxdiff):
                    myaction = a
                    maxdiff = armydiff
    #edited upto this

    if state.turn_type == 'Fortify':
        for a in actions:
            if a.from_territory == None or a.to_territory == None:
                continue
            fort = 1
            for n in state.board.territories[state.board.territory_to_id[a.from_territory]].neighbors:
                if state.owners[n] != state.current_player:
                    fort = 0
                    break
            if fort == 0:
                continue
            for n in state.board.territories[state.board.territory_to_id[a.to_territory]].neighbors:
                if state.owners[n] != state.current_player:
                    myaction  = a
        return myaction
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
            #s = myaction.print_action()
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
    if state.turn_type == 'Place' or state.turn_type == 'PrePlace':
        possible_actions = []

        for a in actions:
            if a.to_territory is not None:
                for n in state.board.territories[state.board.territory_to_id[a.to_territory]].neighbors:
                    if state.owners[n] != state.current_player:
                        possible_actions.append(a)

        if len(possible_actions) > 0:
            myaction = random.choice(possible_actions)


    return myaction

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
