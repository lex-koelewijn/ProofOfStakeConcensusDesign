# The Effects of Proof-of-Stake Design on Consensus: a Game-Theoretical Simulation-Based Aapproach

This project contains a game theoretical simulation investigating the influence of reward design on the behavior of validators in Proof-of-Stake concensus. It is the code used for the Master thesis "The Effects of Proof-of-Stake Design on Consensus: a Game-Theoretical Simulation-Based Aapproach" by Lex Koelewijn. This project starts with a replication of [1] and extends the simulation framework to include: PoS with Quorum, Delegated Proof-of-Stake, and Byzantine Fault Tolerant Delegated Proof-of-Stake. 


### Code structure
The game file contains four games representing the 4 variations of consensus we investigated. The Game class is a the most basic class which contains all elements shared between all games. Then each indivdual game extends this class and adds new functionality. The main class is where the simulation paramters are defined globally, all games are run, and the results are recorded and saved to plots. 


### Prerequisites
Due to the minimal dependencies most python versions should work. For reference: the version of python used to develop this project was `3.6.15`.
 
Having a Python environment, the required Python dependencies should be installed by: 

``pip install -r requirements.txt``

### How to run
In order to run the code, the main python file should be called: 

``python main.py``

The simulations will run and will print to the terminal the minimum proportion of honest validators at genesis required to reach an honest equilibrium. Furthermore, plots for the games will be generated and saved in the `/img` folder. Note that these outcomes are based on the global parameters provided in the `main.py` file. 


### References

[1] Motepalli, S., & Jacobsen, H. A. (2021, September). Reward mechanism for blockchains using evolutionary game theory. In 2021 3rd Conference on Blockchain Research & Applications for Innovative Networks and Services (BRAINS) (pp. 217-224). IEEE.