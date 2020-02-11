from motifs import *
from tools import *
import pickle

class Simulation(Victim_cheater_motif):
    
    def __init__(self, cheaters, killers, killed, kill_time):
        '''Creates a simulation of a given game.'''
        Victim_cheater_motif.__init__(self, cheaters, killers, killed, kill_time)
        self.sim_kill_time = self.kill_times
        
    def get_players_set(self, match_id):
        '''Obtains the list of killers and victims in a given match.''' 
        self.players = list(set().union(self.killers[match_id], self.killed[match_id]))
        return self.players
        
    def get_edges(self, match_id):
        '''Obtain the edges of each kill in a given match.''' 
        self.edges = [(i, j) for i, j in zip(self.killers[match_id], self.killed[match_id])]
        return self.edges
    
    def get_killer_index(self, ls, match_id):   
        '''Returns a list of indices of who are cheaters in the killers list.'''
        return [i for i, j in enumerate(ls) if j in self.cheater_killers[match_id]]
        
    def randomize_victims(self):
        '''Creating a new network where offending killers kill non-victim players.'''
        self.get_cheated_games()
        self.get_cheater_killers()
        self.sim_killers = {}
        self.sim_killed = {}
        for i in self.matches:
            if i in self.cheated_games:
                self.sim_killers[i] = []
                self.sim_killed[i] = []
                players = self.get_players_set(i)
                edges = self.get_edges(i)
                tokens = tokenization(players)
                edges_token = [(get_token(tokens, p), get_token(tokens, q)) for p, q in edges]
                index_freeze = self.get_killer_index(players, i)
                players_new = shuffle_with_fix(players, index_freeze)
                new_tokens = tokenization(players_new)
                for p, q in edges_token:
                    killer = new_tokens[p]
                    dead = new_tokens[q]
                    self.sim_killers[i].append(killer)
                    self.sim_killed[i].append(dead)
            else: 
                self.sim_killers[i] = [j for j in self.killers[i]]
                self.sim_killed[i] = [j for j in self.killed[i]] 
        return self.sim_killers, self.sim_killed, self.sim_kill_time
    
    def save_network(self, i):
        '''Saving the simulated network into a pickle file.'''
        pickle_out = open("dict.pickle_killers" + "_" + str(i), "wb")
        pickle.dump(self.sim_killers, pickle_out)
        pickle_out.close()
        pickle_out = open("dict.pickle_killed" + "_" + str(i), "wb")
        pickle.dump(self.sim_killed, pickle_out)
        pickle_out.close()
    

