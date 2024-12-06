class bestScores:
    scores = []  # Class-level list to store all scores
    
    def __init__(self, score):
        self.score = score
        bestScores.scores.append(self.score)  # Append to the class-level list
    
    def bestThreeScores(self):
        sortedScores = sorted(bestScores.scores, reverse=True)
        while len(sortedScores) < 3:
            sortedScores.append(None)
        return sortedScores[:3]
