import numpy as np

class Game:
    def __init__(self, A, h, m, alpha = 1250, rounds = 100, agents = 1000, honest = 0.66, malicious = 0.33) -> None:
        # Initialize simulation parameters
        self.rounds = rounds
        self.numberOfAgents = agents
        self.proportionHonest = honest
        self.proportionMalicious = malicious
        
        # Initialize simulation arrays
        self.agents = []
        self.evolutionHonest = [honest]
        self.evolutionMalicious = [malicious]
        
        # Initialize variable required for fitness calculation and replicator dynamics 
        self.A = A      # Reward matrix
        self.h = h      # Vector representing always honest strategy [1 0]
        self.m = m      # Vector representing always malicious strategy [0 1]
        
        self.alpha = alpha
        self.fitnessHonest = None 
        self.fitnessMalicious = None
        self.fitnessAverage = None
        self.payoffHonestVsHonest = None
        self.payoffHonestVsMalicious = None
        self.payoffMaliciousVsHonest = None
        self.payoffMaliciousVsMalicious = None
    
    # Return array of agents        
    def getAgents(self):
        return self.agents 
    
    # Get current proportion of honest agents
    def getHonest(self):
        return self.proportionHonest

    # Get current proportion of malicious agents
    def getMalicious(self):
        return self.proportionMalicious
    
    # Get array containing proportion of honest agents over time 
    def getEvolutionHonest(self):
        return self.evolutionHonest
    
    # Get array containing proportion of malicious agents over time 
    def getEvolutionMalicious(self):
        return self.evolutionMalicious
        
class MotepalliGame(Game):
    
    def playGame(self):
        # Use linear algebra to calculate the payoffs of each possible strategy pairing
        self.payoffHonestVsHonest = np.matmul(np.matmul(self.h,self.A),self.h)
        self.payoffMaliciousVsMalicious = np.matmul(np.matmul(self.m,self.A),self.m)
        self.payoffHonestVsMalicious = np.matmul(np.matmul(self.h,self.A),self.m)
        self.payoffMaliciousVsHonest = np.matmul(np.matmul(self.m,self.A),self.h)
        
        for i in range(self.rounds):
            # Calculate fitness of strategy based on payoff and probability of encoutering each type of agent
            self.fitnessHonest = self.proportionHonest*self.payoffHonestVsHonest + self.proportionMalicious * self.payoffHonestVsMalicious 
            self.fitnessMalicious = self.proportionHonest*self.payoffMaliciousVsHonest + self.proportionMalicious * self.payoffMaliciousVsMalicious
            self.fitnessAverage = self.proportionHonest * self.fitnessHonest + self.proportionMalicious * self.fitnessMalicious
            
            # Calculate new proportion of honest vs malicious agents based on replicator dynamics
            self.proportionHonest = ((self.alpha + self.fitnessHonest)/(self.alpha + self.fitnessAverage))*self.proportionHonest
            self.proportionMalicious = ((self.alpha + self.fitnessMalicious)/(self.alpha + self.fitnessAverage))*self.proportionMalicious
            
            # Append newly calculated propotions to the evolution
            self.evolutionHonest.append(self.proportionHonest)
            self.evolutionMalicious.append(self.proportionMalicious)

class QuorumGame(Game):
    def __init__(self, A, h, m, mu = 0.0, alpha = 1250, rounds = 100, agents = 1000, honest = 0.66, malicious = 0.33) -> None:
        # Call constructor of the parent Game class
        super().__init__(A, h, m, alpha, rounds, agents, honest, malicious)
        
        # Initialize paramters to be added on top of base Game class
        self.probabilityHonestQuorum = None
        self.probabilityMaliciousQuorum = None 
        self.probabilityCommitteeMalfunction = mu
    
    def playGame(self):
        # Use linear algebra to calculate the payoffs of each possible strategy pairing
        self.payoffHonestVsHonest = np.matmul(np.matmul(self.h,self.A),self.h)
        self.payoffMaliciousVsMalicious = np.matmul(np.matmul(self.m,self.A),self.m)
        self.payoffHonestVsMalicious = np.matmul(np.matmul(self.h,self.A),self.m)
        self.payoffMaliciousVsHonest = np.matmul(np.matmul(self.m,self.A),self.h)
        
        for i in range(self.rounds):
            quorumRewardHonest = 0.0
            quorumRewardMalicious = 0.0
            self.probabilityHonestQuorum = None
            self.probabilityMaliciousQuorum = None
            
            if( np.random.random() <  self.probabilityCommitteeMalfunction):
                self.probabilityMaliciousQuorum = 1.0 
                self.probabilityHonestQuorum = 0.0
                quorumRewardMalicious = 10
            else:
                # Honest agents wish to reach an honest quorum and gain extra utility for that. The other scenarios are worthless to them.
                # Malicious agents gain utility when reaching a malicious quorum or when no quorum is reached, seeing as sabotaging the system might benefit them.
                if(self.proportionHonest >= 0.66):
                    self.probabilityHonestQuorum = 1.0
                    quorumRewardHonest = 10
                elif(self.proportionHonest < 0.66):
                    self.probabilityHonestQuorum = 0.0 
                    quorumRewardMalicious = 10
                    
                if(self.proportionMalicious >= 0.66):
                    self.probabilityMaliciousQuorum = 1.0
                    quorumRewardMalicious = 10
                elif(self.proportionMalicious < 0.66):
                    self.probabilityMaliciousQuorum = 0.0
                    quorumRewardMalicious = 10
            
            # Calculate fitness of strategy based on payoff and probability of encountering each type of agent
            self.fitnessHonest = self.probabilityHonestQuorum*self.payoffHonestVsHonest + self.probabilityMaliciousQuorum * self.payoffHonestVsMalicious + quorumRewardHonest
            self.fitnessMalicious = self.probabilityHonestQuorum*self.payoffMaliciousVsHonest + self.probabilityMaliciousQuorum * self.payoffMaliciousVsMalicious + quorumRewardMalicious
            self.fitnessAverage = self.proportionHonest * self.fitnessHonest + self.proportionMalicious * self.fitnessMalicious
            
            # Calculate new proportion of honest vs malicious agents based on replicator dynamics
            self.proportionHonest = ((self.alpha + self.fitnessHonest)/(self.alpha + self.fitnessAverage))*self.proportionHonest
            self.proportionMalicious = ((self.alpha + self.fitnessMalicious)/(self.alpha + self.fitnessAverage))*self.proportionMalicious
            
            # Append newly calculated propotions to the evolution
            self.evolutionHonest.append(self.proportionHonest)
            self.evolutionMalicious.append(self.proportionMalicious)
            

class dPOSGame(Game):
    def playGame(self):
        # Use linear algebra to calculate the payoffs of each possible strategy pairing
        self.payoffHonestVsHonest = np.dot(self.A, self.h)
        self.payoffMaliciousVsMalicious = np.dot(self.A, self.m)
        self.payoffHonestVsMalicious = np.dot(self.A, self.h)
        self.payoffMaliciousVsHonest = np.dot(self.A, self.m)
        
        for i in range(self.rounds):
            # Calculate fitness of strategy based on payoff and probability of encoutering each type of agent
            self.fitnessHonest = self.proportionHonest*self.payoffHonestVsHonest + self.proportionMalicious * self.payoffHonestVsMalicious 
            self.fitnessMalicious = self.proportionHonest*self.payoffMaliciousVsHonest + self.proportionMalicious * self.payoffMaliciousVsMalicious
            self.fitnessAverage = self.proportionHonest * self.fitnessHonest + self.proportionMalicious * self.fitnessMalicious
            
            # Calculate new proportion of honest vs malicious agents based on replicator dynamics
            self.proportionHonest = ((self.alpha + self.fitnessHonest)/(self.alpha + self.fitnessAverage))*self.proportionHonest
            self.proportionMalicious = ((self.alpha + self.fitnessMalicious)/(self.alpha + self.fitnessAverage))*self.proportionMalicious
            
            # Append newly calculated propotions to the evolution
            self.evolutionHonest.append(self.proportionHonest)
            self.evolutionMalicious.append(self.proportionMalicious)

class dPOSBFTGame(Game):
    def __init__(self, A, h, m, mu = 0.0, alpha = 1250, rounds = 100, agents = 1000, honest = 0.66, malicious = 0.33) -> None:
        # Call constructor of the parent Game class
        super().__init__(A, h, m, alpha, rounds, agents, honest, malicious)
        
        # Initialize paramters to be added on top of base Game class
        self.probabilityHonestQuorum = None
        self.probabilityMaliciousQuorum = None
        self.probabilityCommitteeMalfunction = mu
    
    def playGame(self):
        # Use linear algebra to calculate the payoffs of each possible strategy pairing
        self.payoffHonestVsHonest = np.matmul(np.matmul(self.h,self.A),self.h)
        self.payoffMaliciousVsMalicious = np.matmul(np.matmul(self.m,self.A),self.m)
        self.payoffHonestVsMalicious = np.matmul(np.matmul(self.h,self.A),self.m)
        self.payoffMaliciousVsHonest = np.matmul(np.matmul(self.m,self.A),self.h)
        
        for i in range(self.rounds):
            quorumRewardHonest = 0.0
            quorumRewardMalicious = 0.0
            self.probabilityHonestQuorum = None
            self.probabilityMaliciousQuorum = None
            
            # With random chance, the committee will malfunction and a malicious quorum will occur
            if( np.random.random() <  self.probabilityCommitteeMalfunction):
                self.probabilityMaliciousQuorum = 1.0
                self.probabilityHonestQuorum = 0.0 
                quorumRewardMalicious = 10
            else:
                # Honest agents wish to reach an honest quorum and gain extra utility for that. The other scenarios are worthless to them.
                # Malicious agents gain utility when reaching a malicious quorum or when no quorum is reached, seeing as sabotaging the system might benefit them.
                if(self.proportionHonest >= 0.66):
                    self.probabilityHonestQuorum = 1.0 
                    quorumRewardHonest = 10
                elif(self.proportionHonest < 0.66):
                    self.probabilityHonestQuorum = 0.0
                    quorumRewardMalicious = 10
                    
                if(self.proportionMalicious >= 0.66):
                    self.probabilityMaliciousQuorum = 1.0
                    quorumRewardMalicious = 10
                elif(self.proportionMalicious < 0.66):
                    self.probabilityMaliciousQuorum = 0.0
                    quorumRewardMalicious = 10
            
            # Calculate fitness of strategy based on payoff and probability of encoutering each type of agent
            self.fitnessHonest = self.probabilityHonestQuorum*self.payoffHonestVsHonest + self.probabilityMaliciousQuorum * self.payoffHonestVsMalicious + quorumRewardHonest
            self.fitnessMalicious = self.probabilityHonestQuorum*self.payoffMaliciousVsHonest + self.probabilityMaliciousQuorum * self.payoffMaliciousVsMalicious + quorumRewardMalicious
            self.fitnessAverage = self.proportionHonest * self.fitnessHonest + self.proportionMalicious * self.fitnessMalicious
            
            # Calculate new proportion of honest vs malicious agents based on replicator dynamics
            self.proportionHonest = ((self.alpha + self.fitnessHonest)/(self.alpha + self.fitnessAverage))*self.proportionHonest
            self.proportionMalicious = ((self.alpha + self.fitnessMalicious)/(self.alpha + self.fitnessAverage))*self.proportionMalicious
            
            # Append newly calculated propotions to the evolution
            self.evolutionHonest.append(self.proportionHonest)
            self.evolutionMalicious.append(self.proportionMalicious)
