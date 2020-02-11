##import required modules## 
from collections import defaultdict
from tools import *

class Victim_cheater_motif(object):
    
    def __init__(self, cheaters, killers, killed, kill_time):
        '''Creates lists of cheaters and their victims.'''
        self.cheaters = cheaters.keys()
        self.matches = killers.keys()
        self.killers = killers
        self.killed = killed
        self.offending_times = cheaters
        self.kill_times = kill_time
        
    def get_offending_time(self, player_id):
        '''Obtaining the estimated time when the given player starts their offense.'''
        return self.offending_times[player_id][0]
        
    def get_cheater_killers(self):    
        '''Identify killers who are cheaters in the game and obtaining their position in a given game'''
        self.cheater_killers = defaultdict(lambda: '0')
        self.cheater_killers_index = defaultdict(lambda: '0')
        for i in self.matches:
            if overlapping_lists(self.killers[i], self.cheaters):
                self.cheater_killers[i] = [q for p, q in intersection(self.killers[i], self.cheaters) 
                                      if get_duration(fmt = '%Y-%m-%d %H:%M:%S', start = self.get_offending_time(q),
                                                        end = self.kill_times[i][p]) > timedelta(seconds = 0)]
                self.cheater_killers_index[i] = [p for p, q in intersection(self.killers[i], self.cheaters) 
                                      if get_duration(fmt = '%Y-%m-%d %H:%M:%S', start = self.get_offending_time(q),
                                                        end = self.kill_times[i][p]) > timedelta(seconds = 0)]
        return self.cheater_killers, self.cheater_killers_index
            
    def get_cheated_games(self):    
        '''IDs of matches containing offending killers.'''
        self.get_cheater_killers()
        self.cheated_games = self.cheater_killers.keys()
        return self.cheated_games
            
    def get_victims(self):   
        '''Identify players who are killed by cheaters.'''
        self.get_cheated_games()
        self.victims = defaultdict(lambda: '0')
        for i in self.cheated_games:
            self.victims[i] = [self.killed[i][j] for j in self.cheater_killers_index[i]]
        return self.victims
    
    def get_victim_killed_time(self):
        '''Obtaining the time when the victim is killed in a given game.'''
        self.get_victims()
        self.victim_killed_time = defaultdict(lambda: '0')
        for i in self.cheated_games:
            self.victim_killed_time[i] = [self.kill_times[i][j] for j in self.cheater_killers_index[i]]
        return self.victim_killed_time
    
    def get_victim_cheaters(self):   
        '''Identify victims who become cheaters.'''
        self.get_victim_killed_time()
        self.victim_cheaters = defaultdict(lambda: '0')
        self.victim_cheaters_index = defaultdict(lambda: '0')
        self.victim_killers = defaultdict(lambda: '0')
        for i in self.matches:
            if overlapping_lists(self.victims[i], self.cheaters):
                self.victim_cheaters[i] = [q for p, q in intersection(self.victims[i], self.cheaters)]
                self.victim_cheaters_index[i] = [p for p, q in intersection(self.victims[i], self.cheaters)]
        return self.victim_cheaters, self.victim_cheaters_index
        
    def get_cheater_killed_time(self):  
        '''Identify the time when the offending victim were killed.'''
        self.get_victim_cheaters()
        self.cheater_killed_time = defaultdict(lambda: '0')
        for i in self.victim_cheaters.keys():
            self.cheater_killed_time[i] = [self.victim_killed_time[i][j] for j in self.victim_cheaters_index[i]]
        return self.cheater_killed_time    
                       
    def count_motifs(self, fmt):     
        '''Counting all victim-cheater motifs in a given game.'''
        self.get_cheater_killed_time()
        self.motifs= defaultdict(lambda: '0')
        for k in self.victim_cheaters.keys():
            self.motifs[k] = []
            for i,j in enumerate(self.cheater_killed_time[k]):
                player_id = self.victim_cheaters[k][i]
                duration = get_duration(fmt, j, self.get_offending_time(player_id))
                if (duration <= timedelta(days = 5) and duration >= timedelta(seconds = 0)):
                    self.motifs[k].append(player_id)
        self.motifs = remove_empty_lists(self.motifs)
        return self.motifs

