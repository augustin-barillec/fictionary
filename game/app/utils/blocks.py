import copy
import app.utils as ut


def get_block(basename):
    return ut.jsons.get_json('blocks', basename)


def get_divider_block():
    return get_block('divider.json')


def get_text_block_template():
    return get_block('text.json')


def get_button_block_template():
    return get_block('button.json')


def u(blocks):
    return [get_divider_block()] + blocks


def d(blocks):
    return blocks + [get_divider_block()]


def build_text_block(msg):
    res = get_text_block_template()
    res['text']['text'] = msg
    return res


def build_button_block(msg, id_):
    res = get_button_block_template()
    res['elements'][0]['text']['text'] = msg
    res['block_id'] = id_
    return res


def build_timer_block(time_left, kind):
    assert kind in ('guess', 'vote')
    time_display = ut.time.build_time_display_for_timer(time_left)
    msg = f'Time left to {kind}: {time_display}'
    return build_text_block(msg)


class BlockBuilder:
    def __init__(self, game):
        self.game = game
        self.surface_id_builder = self.game.surface_id_builder

    def build_guess_timer_block(self):
        return build_timer_block(self.game.time_left_to_guess, 'guess')

    def build_vote_timer_block(self):
        return build_timer_block(self.game.time_left_to_vote, 'vote')

    def build_title_block(self):
        if self.game.parameter == 'freestyle':
            kind = 'Freestyle'
        else:
            kind = 'Automatic'
        organizer = ut.users.user_display(self.game.organizer_id)
        msg = f'{kind} game set up by {organizer}!'
        return build_text_block(msg)

    def build_question_block(self):
        return build_text_block(self.game.question)

    @staticmethod
    def build_preparing_guess_stage_block():
        return build_text_block('Preparing guess stage...')

    @staticmethod
    def build_preparing_vote_stage_block():
        return build_text_block('Preparing vote stage...')

    @staticmethod
    def build_computing_results_stage_block():
        return build_text_block('Computing results... :drum_with_drumsticks:')

    def build_guess_button_block(self):
        id_ = self.surface_id_builder.build_guess_button_block_id()
        return build_button_block('Guess', id_)

    def build_vote_button_block(self):
        id_ = self.surface_id_builder.build_vote_button_block_id()
        return build_button_block('Vote', id_)

    def build_nb_remaining_potential_guessers_block(self):
        nb = self.game.nb_remaining_potential_guessers
        msg = f'Potential guessers: {nb}'
        return build_text_block(msg)

    @staticmethod
    def build_users_blocks(users, kind, no_users_msg):
        msg = ut.users.build_users_msg(users, kind, no_users_msg)
        return build_text_block(msg)

    def build_remaining_potential_voters_block(self):
        kind = 'Potential voters'
        no_users_msg = 'Everyone has voted!'
        return self.build_users_blocks(
            self.game.remaining_potential_voters, kind, no_users_msg)

    def build_guessers_block(self):
        users = self.game.guessers
        kind = 'Guessers'
        no_users_msg = 'No one has guessed yet.'
        return self.build_users_blocks(users, kind, no_users_msg)

    def build_voters_block(self):
        users = self.game.voters
        kind = 'Voters'
        no_users_msg = 'No one has voted yet.'
        return self.build_users_blocks(users, kind, no_users_msg)

    def build_indexed_anonymous_proposals_block(self):
        msg = ['Proposals:']
        indexed_anonymous_proposals = \
            ut.proposals.ProposalsBrowser(
                self.game).build_indexed_anonymous_proposals()
        for iap in indexed_anonymous_proposals:
            index = iap['index']
            proposal = iap['proposal']
            msg.append(f'{index}) {proposal}')
        msg = '\n'.join(msg)
        return build_text_block(msg)

    def build_own_guess_block(self, voter):
        index, guess = ut.proposals.ProposalsBrowser(
            self.game).build_own_indexed_guess(voter)
        msg = f'Your guess: {index}) {guess}'
        return build_text_block(msg)

    def build_truth_block(self):
        msg = '• Truth: '
        if len(self.game.frozen_guessers) <= 1:
            msg += f'{self.game.truth}'
        else:
            index = self.game.truth_index
            msg += f'{index}) {self.game.truth}'
        return build_text_block(msg)

    def build_signed_guesses_block(self, show_index):
        msg = []
        for r in copy.deepcopy(self.game.results):
            guesser = ut.users.user_display(r['guesser'])
            index = r['index']
            guess = r['guess']
            if show_index:
                r_msg = f'• {guesser}: {index}) {guess}'
            else:
                r_msg = f'• {guesser}: {guess}'
            msg.append(r_msg)
        msg = '\n'.join(msg)
        return build_text_block(msg)

    def build_signed_noindexed_guesses_block(self):
        return self.build_signed_guesses_block(show_index=False)

    def build_signed_indexed_guesses_block(self):
        return self.build_signed_guesses_block(show_index=True)

    def build_voting_edges_block(self):
        msg = []
        for r in copy.deepcopy(self.game.results):
            if 'vote_index' not in r:
                continue
            voter = ut.users.user_display(r['guesser'])
            chosen_author = r['chosen_author']
            if chosen_author != 'Truth':
                chosen_author = ut.users.user_display(chosen_author)
            r_msg = f'• {voter} -> {chosen_author}'
            msg.append(r_msg)
        msg = '\n'.join(msg)
        return build_text_block(msg)

    def build_scores_block(self):
        msg = []
        for r in copy.deepcopy(self.game.results):
            guesser = ut.users.user_display(r['guesser'])
            score = r['score']
            assert score >= 0
            if score == 1:
                p = f'{score} point'
            else:
                p = f'{score} points'
            r_msg = f'• {guesser}: {p}'
            msg.append(r_msg)
        msg = '\n'.join(msg)
        return build_text_block(msg)

    def build_conclusion_msg(self):
        lg = len(self.game.frozen_guessers)
        lv = len(self.game.frozen_voters)
        lw = len(self.game.winners)
        if lg == 0:
            return 'No one played this game. :sob:'
        elif lg == 1:
            g = ut.users.user_display(list(self.game.frozen_guessers)[0])
            return f'Thanks for your guess, {g}!'
        elif lv == 0:
            return 'No one voted. :sob:'
        elif lv == 1:
            r = self.game.results[0]
            g = ut.users.user_display(r['guesser'])
            ca = r['chosen_author']
            if ca == 'Truth':
                return f'Bravo {g}! You found the truth! :v:'
            return f'Hey {g}, at least you voted! :grimacing:'
        elif self.game.max_score == 0:
            return 'Zero points scored!'
        elif lw == lv:
            return "Well, it's a draw! :scales:"
        elif lw == 1:
            w = ut.users.user_display(self.game.winners[0])
            return f'And the winner is {w}! :first_place_medal:'
        elif lw > 1:
            ws = [ut.users.user_display(w) for w in self.game.winners]
            msg_aux = ','.join(ws[:-1])
            msg_aux += f' and {ws[-1]}'
            return f'And the winners are {msg_aux}! :clap:'

    def build_conclusion_block(self):
        msg = self.build_conclusion_msg()
        return build_text_block(msg)

    def build_pre_guess_stage_upper_blocks(self):
        title_block = self.build_title_block()
        preparing_guess_stage_block = self.build_preparing_guess_stage_block()
        return u([title_block, preparing_guess_stage_block])

    @staticmethod
    def build_pre_guess_stage_lower_blocks():
        return d([])

    def build_pre_vote_stage_upper_blocks(self):
        title_block = self.build_title_block()
        question_block = self.build_question_block()
        preparing_vote_stage_block = self.build_preparing_vote_stage_block()
        return u([title_block, question_block, preparing_vote_stage_block])

    @staticmethod
    def build_pre_vote_stage_lower_blocks():
        return d([])

    def build_pre_result_stage_upper_blocks(self):
        title_block = self.build_title_block()
        question_block = self.build_question_block()
        computing_results_stage_block = \
            self.build_computing_results_stage_block()
        return u([title_block, question_block, computing_results_stage_block])

    @staticmethod
    def build_pre_result_stage_lower_blocks():
        return d([])

    def build_guess_stage_upper_blocks(self):
        title_block = self.build_title_block()
        question_block = self.build_question_block()
        guess_button_block = self.build_guess_button_block()
        return u([title_block, question_block, guess_button_block])

    def build_guess_stage_lower_blocks(self):
        guess_timer_block = self.build_guess_timer_block()
        nb_remaining_potential_guessers_block = \
            self.build_nb_remaining_potential_guessers_block()
        guessers_block = self.build_guessers_block()
        return d([guess_timer_block, nb_remaining_potential_guessers_block,
                  guessers_block])

    def build_vote_stage_upper_blocks(self):
        title_block = self.build_title_block()
        question_block = self.build_question_block()
        anonymous_proposals_block = \
            self.build_indexed_anonymous_proposals_block()
        vote_button_block = self.build_vote_button_block()
        return u([title_block, question_block,
                  anonymous_proposals_block, vote_button_block])

    def build_vote_stage_lower_blocks(self):
        vote_timer_block = self.build_vote_timer_block()
        remaining_potential_voters_block = \
            self.build_remaining_potential_voters_block()
        voters_block = self.build_voters_block()
        return d([vote_timer_block, remaining_potential_voters_block,
                  voters_block])

    def build_result_stage_upper_blocks(self):
        title_block = self.build_title_block()
        question_block = self.build_question_block()
        truth_block = self.build_truth_block()
        signed_noindexed_guesses_block = \
            self.build_signed_noindexed_guesses_block()
        signed_indexed_guesses_block = \
            self.build_signed_indexed_guesses_block()
        voting_edges_block = self.build_voting_edges_block()
        scores_block = self.build_scores_block()
        conclusion_block = self.build_conclusion_block()
        res = [title_block, question_block, truth_block]
        lg = len(self.game.frozen_guessers)
        lv = len(self.game.frozen_voters)
        if lg == 1:
            res.append(signed_noindexed_guesses_block)
        elif lg >= 2:
            res.append(signed_indexed_guesses_block)
            if lv >= 1:
                res += [voting_edges_block, scores_block]
        res.append(conclusion_block)
        res = u(res)
        return res

    @staticmethod
    def build_result_stage_lower_blocks():
        return d([])
