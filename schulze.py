#  This file implements the Schulze method using Floyd-Warshall

def validate(candidates, ballots):
    # Ensure candidates is a list of strings
    if not isinstance(candidates, list):
        return "candidates must be an array"
    for candidate in candidates:
        if not isinstance(candidate, str):
            return "each candidate must be a string"

    n = len(candidates)
    
    # Ensure ballots is a list of lists of integers
    if not isinstance(ballots, list):
        return "ballots must be an array"
    for ballot in ballots:
        if not isinstance(ballot, list):
            return "each ballot must be an array"
        if len(ballot) != n:
            return "each ballot must contain a rank for each candidate"
        for rank in ballot:
            if not isinstance(rank, int):
                return "each candidate in a ballot must be given a number"
    
    return "AllOk"


# Converts ranks into groups of candidates with the same rank
def ranks_to_groups(ranks, candidates):
    by_rank = {}
    # Group candidates by their ranks
    for i, rank in enumerate(ranks):
        if rank not in by_rank:
            by_rank[rank] = []
        by_rank[rank].append(candidates[i])
    
    # Sort ranks and group candidates accordingly
    keys = sorted(by_rank.keys())
    groups = [by_rank[key] for key in keys]
    place = 1
    
    # Format groups with their rank positions
    return [{"place": place + i, "indexes": group} for i, group in enumerate(groups)]

# Converts grouped candidates back to ranks.
def groups_to_ranks(n, groups):
    ranks = [len(groups) + 1] * n       # List of integers representing ranks for each candidate
    for i, group in enumerate(groups):
        for index in group:
            ranks[index] = i + 1
    return ranks

'''
d[i][j]: Number of voters preferring candidate i over candidate j.
p[i][j]: Strength of the strongest path from candidate i to j.

A "path" is a sequence of candidates where voters prefer each candidate in the sequence over the next.
"Strength" of a path b/w i and j: Weakest link of path to go from i->j
'''
def run_schulze(n, ballots, candidates):
    d = [[0] * n for _ in range(n)]         # pairwise preference matrix
    p = [[0] * n for _ in range(n)]         # strongest path matrix
    
    # Compute pairwise preferences
    for ballot in ballots:
        for i in range(n):
            for j in range(n):
                if i != j:
                    if ballot[i] < ballot[j]:
                        d[i][j] += 1
    
    # Compute strongest path strengths - Floyd-Warshall
    for i in range(n):
        for j in range(n):
            if i != j:
                if d[i][j] > d[j][i]:
                    p[i][j] = d[i][j]
                        
    for k in range(n):
        for i in range(n):
            if i != k:
                for j in range(n):
                    if i != j and j != k:
                        p[i][j] = max(p[i][j], min(p[i][k], p[k][j]))
    
    # num wins for each candidate
    wins = [0] * n
    for i in range(n):
        for j in range(n):
            if i != j and p[i][j] > p[j][i]:    # i beats j
                wins[i] += 1
    
    # Rank candidates by the number of wins (negative for sorting in ascending order)
    return ranks_to_groups([-w for w in wins], candidates)
