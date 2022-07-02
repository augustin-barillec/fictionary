from app.utils import proposals


class ResultsBuilder:

    def __init__(self, game):
        self.game = game
        self.proposals_browser = proposals.ProposalsBrowser(self.game)

    def compute_truth_score(self, voter):
        return int(self.game.frozen_voters[voter][1] == self.game.truth_index)

    def compute_bluff_score(self, voter):
        res = 0
        for voter_ in self.game.frozen_voters:
            voter_index = self.proposals_browser.author_to_index(voter)
            if self.game.frozen_voters[voter_][1] == voter_index:
                res += 2
        return res

    def build_results(self):
        results = []
        for isp in self.game.indexed_signed_proposals:
            index = isp['index']
            author = isp['author']
            proposal = isp['proposal']
            r = dict()
            if author == 'Truth':
                continue
            r['index'] = index
            r['guesser'] = author
            r['guess'] = proposal
            if author not in self.game.frozen_voters:
                r['score'] = 0
                results.append(r)
                continue
            vote_index = self.game.frozen_voters[author][1]
            r['vote_index'] = vote_index
            r['chosen_author'] = self.proposals_browser.index_to_author(
                vote_index)
            r['truth_score'] = self.compute_truth_score(author)
            r['bluff_score'] = self.compute_bluff_score(author)
            r['score'] = r['truth_score'] + r['bluff_score']
            results.append(r)

        def sort_key(r_):
            return 'vote_index' not in r_, -r_['score'], r_['guesser']

        results.sort(key=lambda r_: sort_key(r_))

        return results


def compute_max_score(game):
    scores = [r['score'] for r in game.results if 'score' in r]
    if len(scores) == 0:
        return -1
    else:
        return scores[0]


def compute_winners(game):
    res = []
    for r in game.results:
        if r['score'] == game.max_score:
            res.append(r['guesser'])
    return res
