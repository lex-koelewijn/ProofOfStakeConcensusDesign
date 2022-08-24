import numpy as np
import matplotlib.pyplot as plt
from Game import MotepalliGame, QuorumGame, dPOSGame, dPOSBFTGame
from Util import *

# Check is required subdirectories are present
directoryCheck()

#Define rewards to be user through in reward matrix definitions
r = 10              # Block reward:      {10}
p = 100             # Penalty Term:      {90, 100, 110}
b = 100             # Byzantine Reward:  {100}

# Define reward matrix A, honest strategy by vector h, and malicious strategy by vector m
A = np.array([[r, -p], [-p, r+b]])
h = np.array([1.0, 0])
m = np.array ([0, 1.0])

# Global Parameters
_rounds = 1000
_mu = 0.0
_agents = 100
_alpha = 1250
_averagingRuns = 250
_threshold = 0.66
_honest = 0.66
_malicious = 1.0 - _honest

# Instantiate a PoS with Penalties game and run the simulations
game = MotepalliGame(A, h, m, alpha = _alpha, rounds = _rounds, agents = _agents, honest = _honest, malicious = _malicious)
game.playGame()

# Create a plot of the proportion of honest vs malicious over time in the simulation
plt.plot(game.getEvolutionHonest(), label = 'Honest')
plt.plot(game.getEvolutionMalicious(), label = 'Malicious')
plt.legend()
plt.xlabel("Rounds")
plt.ylabel("Propotion of agents")
plt.savefig('img/motepalliGame.png')
plt.savefig('img/all/motepalliGame'+ '_P' + str(p) + '_B' + str(b) + '_Xh' + str(_honest) + '_Th' + str(_threshold)  +'.png')
plt.savefig('img/all/motepalliGame'+ '_P' + str(p) + '_B' + str(b) + '_Xh' + str(_honest) + '_Th' + str(_threshold)  +'.svg')
plt.close()

# Instantiate a PoS with Quorum game and run the simulation
quorumGame = QuorumGame(A, h, m, mu = _mu, alpha = _alpha, rounds = _rounds, agents = _agents, honest = _honest, malicious = _malicious) 
quorumGame.playGame()

# Create a plot of the proportion of honest vs malicious over time in the simulation
plt.plot(quorumGame.getEvolutionHonest(), label = 'Honest')
plt.plot(quorumGame.getEvolutionMalicious(), label = 'Malicious')
plt.legend()
plt.xlabel("Rounds")
plt.ylabel("Propotion of agents")
plt.savefig('img/QuorumGame.png')
plt.savefig('img/all/QuorumGame'+ '_P' + str(p) + '_B' + str(b) + '_Xh' + str(_honest) + '_Th' + str(_threshold)  +'.png')
plt.savefig('img/all/QuorumGame'+ '_P' + str(p) + '_B' + str(b) + '_Xh' + str(_honest) + '_Th' + str(_threshold)  +'.svg')
plt.close()

# Define reward matrix A for DPoS, honest strategy by vector h, and malicious strategy by vector m
A_dPOS = np.array([r, r+b-p])
h = np.array([1.0, 0])
m = np.array ([0, 1.0])

# Instantiate a DPoS game and run the simulation
dPOS_game = dPOSGame(A_dPOS, h, m, alpha = _alpha, rounds = _rounds, agents = _agents, honest = _honest, malicious = _malicious)
dPOS_game.playGame()

# Create a plot of the proportion of honest vs malicious over time in the simulation
plt.plot(dPOS_game.getEvolutionHonest(), label = 'Honest')
plt.plot(dPOS_game.getEvolutionMalicious(), label = 'Malicious')
plt.legend()
plt.xlabel("Rounds")
plt.ylabel("Propotion of agents")
plt.savefig('img/dPOSGame.png')
plt.savefig('img/all/dPOSGame'+ '_P' + str(p) + '_B' + str(b) + '_Xh' + str(_honest) + '_Th' + str(_threshold)  +'.png')
plt.savefig('img/all/dPOSGame'+ '_P' + str(p) + '_B' + str(b) + '_Xh' + str(_honest) + '_Th' + str(_threshold)  +'.svg')
plt.close()

# Define reward matrix A, honest strategy by vector h, and malicious strategy by vector m under assumption of honest voting
A_dPOS_BFT = np.array([[r, 0], [-p, r+b-p]])
h = np.array([1.0, 0])
m = np.array ([0, 1.0])

# Instantiate a DPoS-BFT game and run the simulation
dPOS_BFT_game = dPOSBFTGame(A_dPOS_BFT, h, m, mu = _mu, alpha = _alpha, rounds = _rounds, agents = _agents, honest = _honest, malicious = _malicious)
dPOS_BFT_game.playGame()

# Create a plot of the proportion of honest vs malicious over time in the simulation
plt.plot(dPOS_BFT_game.getEvolutionHonest(), label = 'Honest')
plt.plot(dPOS_BFT_game.getEvolutionMalicious(), label = 'Malicious')
plt.legend()
plt.xlabel("Rounds")
plt.ylabel("Propotion of agents")
plt.savefig('img/dPOSBFTGame.png')
plt.savefig('img/all/dPOSBFTGame'+ '_P' + str(p) + '_B' + str(b) + '_Xh' + str(_honest) + '_Th' + str(_threshold)  +'.png')
plt.savefig('img/all/dPOSBFTGame'+ '_P' + str(p) + '_B' + str(b) + '_Xh' + str(_honest) + '_Th' + str(_threshold)  +'.svg')
plt.close()


# This function goes through all the games again and uses a gridsearch to find the minimum starting proportion of honest validators such
# that the resulting end state has an honest majority. In fact, the resulting state should be roughly 100% honest validators as the malicious
# invaders will die out. We create a graph and save the cutoff point. 
def gridSearchProportion(_alpha = _alpha, _agents = _agents, _rounds = _rounds, threshold = _threshold) -> dict:
    results = {'MotepalliGame' : [], 'quorumGame': [], 'dPOS_game': [], 'dPOS_BFT_game': [], 'dPOS_BFT_game_no_assumptions': [], 
               'MotepalliGameMin': None, 'quorumGameMin': None, 'dPOS_gameMin': None, 'dPOS_BFT_gameMin': None, 'dPOS_BFT_game_no_assumptionsMin': None}
    
    for i in np.arange(0.0, 1.0, 0.01):
        # MotepalliGame or PoS with Penalties
        game = MotepalliGame(A, h, m, alpha = _alpha, rounds = _rounds, agents = _agents, honest = i, malicious = (1.0-i))
        game.playGame()
        results['MotepalliGame'].append(game.getHonest())
        if(game.getHonest() > threshold and results['MotepalliGameMin'] == None): results['MotepalliGameMin'] = i
        
        # Quorum Game 
        quorumGame = QuorumGame(A, h, m, alpha = _alpha, rounds = _rounds, agents = _agents, honest = i, malicious = (1.0-i)) 
        quorumGame.playGame()
        results['quorumGame'].append(quorumGame.getHonest())
        if(quorumGame.getHonest() > threshold and results['quorumGameMin'] == None): results['quorumGameMin'] = i
        
        # Pure DPOS Game
        dPOS_game = dPOSGame(A_dPOS, h, m, alpha = _alpha, rounds = _rounds, agents = _agents, honest = i, malicious = (1.0-i))
        dPOS_game.playGame()
        results['dPOS_game'].append(dPOS_game.getHonest())
        if(dPOS_game.getHonest() > threshold and results['dPOS_gameMin'] == None): results['dPOS_gameMin'] = i
        
        # dPOS-BFT Game
        dPOS_BFT_game = dPOSBFTGame(A_dPOS_BFT, h, m, mu = _mu, alpha = _alpha, rounds = _rounds, agents = _agents, honest = i, malicious = (1.0-i))
        dPOS_BFT_game.playGame()
        results['dPOS_BFT_game'].append(dPOS_BFT_game.getHonest())
        if(dPOS_BFT_game.getHonest() > threshold and results['dPOS_BFT_gameMin'] == None): results['dPOS_BFT_gameMin'] = i
        
            
    plt.plot(np.arange(0.0, 1.0, 0.01), results['MotepalliGame'], label = 'MotepalliGame')
    plt.plot(np.arange(0.0, 1.0, 0.01), results['quorumGame'], label = 'quorumGame')
    plt.plot(np.arange(0.0, 1.0, 0.01), results['dPOS_game'], label = 'dPOS_game')
    plt.plot(np.arange(0.0, 1.0, 0.01), results['dPOS_BFT_game'], label = 'dPOS_BFT_game')
    plt.xlabel("Starting Proportion of honest agents")
    plt.ylabel("Ending Propotion of honest agents")
    plt.legend()
    plt.savefig('img/comparisson_between_consensus.png')
    plt.close()

    return results

# Run the gridsearch function and print the minimum starting proportion of honest validators required to still reach an honest equilibrium.    
values = gridSearchProportion()
print('MotepalliGameMin: ', values['MotepalliGameMin'])
print('quorumGameMin: ', values['quorumGameMin'])
print('dPOS_gameMin: ', values['dPOS_gameMin'])
print('dPOS_BFT_gameMin: ', values['dPOS_BFT_gameMin'])

# This function tests the effects of an increase in the probability of a random quorum failure.
# The value mu is initialized at 0.0 and increases to 1.0 with steps of 0.01. 
# For each value of mu, a game is created and the ending proportion of honest validators is recorded. 
# For each value of mu, the results are averaged over multiple runs due to the randomness introduced by this mechanism
def testQuorumFailure(threshold = _threshold) -> dict:
    results = {'dPOS-BFT': {'propHonest': [], 'maxMu': None}, 'Quorum': {'propHonest': [], 'maxMu': None}}
    
    for i in np.arange(0.0, 1.0, 0.01):
        avg_end_prop_honest_dposBFT = []
        avg_end_prop_honest_quorum = [] 
        for j in range(0, _averagingRuns):
            # dPOS-BFT:
            dPOS_BFT_game = dPOSBFTGame(A_dPOS_BFT, h, m, mu = i , alpha = _alpha, rounds = _rounds, agents = _agents, honest = _honest, malicious = _malicious)
            dPOS_BFT_game.playGame()
            avg_end_prop_honest_dposBFT.append(dPOS_BFT_game.getHonest())
            
            #Quorum:
            quorumGame = QuorumGame(A, h, m, mu = i, alpha = _alpha, rounds = _rounds, agents = _agents, honest = _honest, malicious =_malicious) 
            quorumGame.playGame()
            avg_end_prop_honest_quorum.append(quorumGame.getHonest())
        
        # dPOS-BFT
        results['dPOS-BFT']['propHonest'].append(np.mean(avg_end_prop_honest_dposBFT))
        if(np.mean(avg_end_prop_honest_dposBFT) < threshold and results['dPOS-BFT']['maxMu'] == None): 
            results['dPOS-BFT']['maxMu'] = i
        # Quorum    
        results['Quorum']['propHonest'].append(np.mean(avg_end_prop_honest_quorum))
        if(np.mean(avg_end_prop_honest_quorum) < threshold and results['Quorum']['maxMu'] == None): 
            results['Quorum']['maxMu'] = i
    
    return results

# Run the quorum failure function and print the maximum value of mu tolerated 
muDict = testQuorumFailure()
print('mu Max dPOS-BFT: ', muDict['dPOS-BFT']['maxMu'])
print('mu Max Quorum: ', muDict['Quorum']['maxMu'])


# Create a plot displaying the ending proportion of honest agents as the value of mu increases
plt.plot(np.arange(0.0, 1.0, 0.01),  muDict['dPOS-BFT']['propHonest'], label = 'dPOS-BFT')
plt.plot(np.arange(0.0, 1.0, 0.01),  muDict['Quorum']['propHonest'], label = 'Quorum')
plt.legend()
plt.xlabel("Probability of quorum failure")
plt.ylabel("Ending propotion of honest agents")
plt.savefig('img/mu.png')
plt.savefig('img/all/mu'+ '_P' + str(p) + '_B' + str(b) + '_Xh' + str(_honest) + '_Th' + str(_threshold)  + '_avg' + str(_averagingRuns) + '.png')
plt.savefig('img/all/mu'+ '_P' + str(p) + '_B' + str(b) + '_Xh' + str(_honest) + '_Th' + str(_threshold)  + '_avg' + str(_averagingRuns) +'.svg')
plt.close()