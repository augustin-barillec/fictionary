from copy import deepcopy
from app.utils import jsons, proposals, time, users


def get_block(basename):
    return jsons.get_json('blocks', basename)


def get_divider_block():
    return get_block('divider.json')


def get_text_block_template():
    return get_block('text.json')


def get_button_block_template():
    return get_block('button.json')


def get_image_block_template():
    return get_block('image.json')


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
    time_display = time.build_time_display_for_timer(time_left)
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
        organizer = users.user_display(self.game.organizer_id)
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
        return build_text_block('Computing results :drum_with_drumsticks:')

    def build_guess_button_block(self):
        id_ = self.surface_id_builder.build_guess_button_block_id()
        return build_button_block('Guess', id_)

    def build_vote_button_block(self):
        id_ = self.surface_id_builder.build_vote_button_block_id()
        return build_button_block('Vote', id_)

    def build_nb_remaining_potential_guessers_block(self):
        x = self.game.nb_remaining_potential_guessers
        msg = f'Potential guessers: {x}'
        return build_text_block(msg)

    @staticmethod
    def build_users_blocks(users_, kind, no_users_msg):
        msg = users.build_users_msg(users_, kind, no_users_msg)
        return build_text_block(msg)

    def build_remaining_potential_voters_block(self):
        kind = 'Potential voters'
        no_users_msg = 'Everyone has voted!'
        return self.build_users_blocks(
            self.game.remaining_potential_voters, kind, no_users_msg)

    def build_guessers_block(self):
        users_ = self.game.guessers
        kind = 'Guessers'
        no_users_msg = 'No one has guessed yet.'
        return self.build_users_blocks(users_, kind, no_users_msg)

    def build_voters_block(self):
        users_ = self.game.voters
        kind = 'Voters'
        no_users_msg = 'No one has voted yet.'
        return self.build_users_blocks(users_, kind, no_users_msg)

    def build_indexed_anonymous_proposals_block(self):
        msg = ['Proposals:']
        indexed_anonymous_proposals = \
            proposals.ProposalsBrowser(
                self.game).build_indexed_anonymous_proposals()
        for iap in indexed_anonymous_proposals:
            index = iap['index']
            proposal = iap['proposal']
            msg.append(f'{index}) {proposal}')
        msg = '\n'.join(msg)
        return build_text_block(msg)

    def build_own_guess_block(self, voter):
        index, guess = proposals.ProposalsBrowser(
            self.game).build_own_indexed_guess(voter)
        msg = f'Your guess: {index}) {guess}'
        return build_text_block(msg)

    def build_truth_block(self):
        msg = '• Truth: '
        if len(self.game.frozen_guessers) == 0:
            msg += f'{self.game.truth}'
        else:
            index = self.game.truth_index
            msg += f'{index}) {self.game.truth}'
        return build_text_block(msg)

    def build_indexed_signed_guesses_block(self):
        msg = []
        for r in deepcopy(self.game.results):
            guesser = users.user_display(r['guesser'])
            index = r['index']
            guess = r['guess']
            r_msg = f'• {guesser}: {index}) {guess}'
            msg.append(r_msg)
        msg = '\n'.join(msg)
        return build_text_block(msg)

    def build_voting_edges_block(self):
        msg = []
        for r in deepcopy(self.game.results):
            if 'vote_index' not in r:
                continue
            voter = users.user_display(r['guesser'])
            chosen_author = r['chosen_author']
            if chosen_author != 'Truth':
                chosen_author = users.user_display(chosen_author)
            r_msg = f'• {voter} -> {chosen_author}'
            msg.append(r_msg)
        msg = '\n'.join(msg)
        return build_text_block(msg)

    def build_scores_block(self):
        msg = []
        for r in deepcopy(self.game.results):
            guesser = users.user_display(r['guesser'])
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
        if lg == 0:
            return 'No one played this game :sob:.'
        if lg == 1:
            g = users.user_display(list(self.game.frozen_guessers)[0])
            return f'Thanks for your guess, {g}!'
        if lv == 0:
            return 'No one voted :sob:.'
        if lv == 1:
            r = self.game.results[0]
            g = users.user_display(r['guesser'])
            ca = r['chosen_author']
            if ca == 'Truth':
                return f'Bravo {g}! You found the truth! :v:'
            else:
                return f'Hey {g}, at least you voted! :grimacing:'
        if self.game.max_score == 0:
            return 'Zero points scored!'
        lw = len(self.game.winners)
        if lw == lv:
            return "Well, it's a draw! :scales:"
        if lw == 1:
            w = users.user_display(self.game.winners[0])
            return f'And the winner is {w}! :first_place_medal:'
        if lw > 1:
            ws = [users.user_display(w) for w in self.game.winners]
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
        res = [title_block, question_block, truth_block]
        lg = len(self.game.frozen_guessers)
        lv = len(self.game.frozen_voters)
        if lg >= 1:
            res.append(self.build_indexed_signed_guesses_block())
        if lg >= 2 and lv >= 1:
            res.append(self.build_voting_edges_block())
            res.append(self.build_scores_block())
        res.append(self.build_conclusion_block())
        res = u(res)
        return res

    @staticmethod
    def build_result_stage_lower_blocks():
        return d([])
