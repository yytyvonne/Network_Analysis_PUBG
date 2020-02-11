def read_cheater(f):
    '''Reads the text file containing the data of cheaters in the game.
    Returns the account ID, start time and quitting time of the cheater'''
    cheaters = {}
    
    for line in f:
        line = line.strip().split()
        cheaters[line[0]] = [line[1] + " " + '00:00:00', line[2] + " " + '00:00:00']
    
    return cheaters

def read_kills(f):
    '''Reads the text file containing the data of all kills during the period
    given. Returns the match ID, account ID of the killer, the victim and time of 
    the kill.'''
    killers = {}
    killed = {}
    kill_time = {}
    
    for line in f:
        line = line.strip().split()
        if line[0] not in killers.keys():
            killers[line[0]] = [line[1]]
            killed[line[0]] = [line[2]]
            kill_time[line[0]] = [line[3] + " " + line[4][:8]]
        else:
            killers[line[0]].append(line[1])
            killed[line[0]].append(line[2])
            kill_time[line[0]].append(line[3] + " " + line[4][:8])
    
    return killers, killed, kill_time