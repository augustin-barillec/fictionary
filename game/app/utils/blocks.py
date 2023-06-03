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


def build_button_block(id_, msg):
    res = get_button_block_template()
    res['elements'][0]['text']['text'] = msg
    res['block_id'] = id_
    return res


def build_timer_block(language, msg_template, time_left):
    time_display = ut.time.build_time_display_for_timer(language, time_left)
    msg = msg_template.format(time_display=time_display)
    return build_text_block(msg)


def build_users_block(msg_template, users, no_users_msg):
    if not users:
        msg = no_users_msg
    else:
        user_ids = ut.users.sort_users(users)
        user_displays = ut.users.users_display(user_ids)
        msg = msg_template.format(user_displays=user_displays)
    return build_text_block(msg)


class BlockBuilder:
    def __init__(self, game):
        self.game = game
        self.language = self.game.language

    def build_guess_timer_block(self):
        msg_template = ut.text.time_left_to_answer[self.language]
        time_left = self.game.time_left_to_guess
        return build_timer_block(self.language, msg_template, time_left)

    def build_vote_timer_block(self):
        msg_template = ut.text.time_left_to_vote[self.language]
        time_left = self.game.time_left_to_vote
        return build_timer_block(self.language, msg_template, time_left)

    def build_title_block(self):
        assert self.game.parameter in ('freestyle', 'automatic')
        organizer_display = ut.users.user_display(self.game.organizer_id)
        msg = None
        if self.game.parameter == 'freestyle':
            msg = ut.text.question_and_answer_written_by[self.language].format(
                organizer_display=organizer_display)
        elif self.game.parameter == 'automatic':
            msg = ut.text.question_selected_by[self.language].format(
                organizer_display=organizer_display)
        return build_text_block(msg)

    def build_question_block(self):
        return build_text_block(self.game.question)

    def build_preparing_guess_stage_block(self):
        return build_text_block(ut.text.loading_the_game[self.language])

    def build_preparing_vote_stage_block(self):
        return build_text_block(
            ut.text.loading_the_voting_stage[self.language])

    def build_computing_results_stage_block(self):
        return build_text_block(ut.text.loading_the_results[self.language])

    def build_guess_button_block(self):
        id_ = self.game.surface_id_builder.build_guess_button_block_id()
        msg = ut.text.answer[self.language]
        return build_button_block(id_, msg)

    def build_vote_button_block(self):
        id_ = self.game.surface_id_builder.build_vote_button_block_id()
        msg = ut.text.vote[self.language]
        return build_button_block(id_, msg)

    def build_nb_remaining_potential_guessers_block(self):
        nb = self.game.nb_remaining_potential_guessers
        msg = ut.text.remaining_spots[self.language].format(nb=nb)
        return build_text_block(msg)

    def build_remaining_potential_voters_block(self):
        msg_template = ut.text.eligible_to_vote[self.language]
        users = self.game.remaining_potential_voters
        no_users_msg = ut.text.all_players_have_voted[self.language]
        return build_users_block(msg_template, users, no_users_msg)

    def build_guessers_block(self):
        msg_template = ut.text.players[self.language]
        users = self.game.guessers
        no_users_msg = ut.text.no_one_has_answered_yet[self.language]
        return build_users_block(msg_template,users, no_users_msg)

    def build_voters_block(self):
        msg_template = ut.text.players_who_voted[self.language]
        users = self.game.voters
        no_users_msg = ut.text.no_one_has_voted_yet[self.language]
        return build_users_block(msg_template, users, no_users_msg)

    def build_indexed_anonymous_proposals_block(self):
        msg = [ut.text.answers[self.language]]
        indexed_anonymous_proposals = \
            ut.proposals.ProposalsBrowser(
                self.game).build_indexed_anonymous_proposals()
        for iap in indexed_anonymous_proposals:
            index = iap['index']
            proposal = iap['proposal']
            msg.append(ut.text.index_proposal[self.language].format(
                index=index, proposal=proposal))
        msg = '\n'.join(msg)
        return build_text_block(msg)

    def build_truth_block(self):
        if len(self.game.frozen_guessers) <= 1:
            msg = ut.text.game_answer_truth[self.language].format(
                truth=self.game.truth)
        else:
            index = self.game.truth_index
            msg = ut.text.game_answer_index_truth[self.language].format(
                index=index, truth=self.game.truth)
        return build_text_block(msg)

    def build_signed_guesses_block(self, show_index):
        msg = []
        for r in self.game.results:
            guesser_display = ut.users.user_display(r['guesser'])
            index = r['index']
            guess = r['guess']
            if show_index:
                r_msg = ut.text.guesser_index_guess[self.language].format(
                    guesser_display=guesser_display,
                    index=index, guess=guess)
            else:
                r_msg = ut.text.guesser_guess[self.language].format(
                    guesser_display=guesser_display, guess=guess)
            msg.append(r_msg)
        msg = '\n'.join(msg)
        return build_text_block(msg)

    def build_signed_noindexed_guesses_block(self):
        return self.build_signed_guesses_block(show_index=False)

    def build_signed_indexed_guesses_block(self):
        return self.build_signed_guesses_block(show_index=True)

    def build_voting_edges_block(self):
        msg = []
        for r in self.game.results:
            if 'vote_index' not in r:
                continue
            voter_display = ut.users.user_display(r['guesser'])
            chosen_author = r['chosen_author']
            if chosen_author == 'Truth':
                r_msg = ut.text.voter_to_game_answer[self.language].format(
                    voter_display=voter_display)
            else:
                chosen_author_display = ut.users.user_display(chosen_author)
                r_msg = ut.text.voter_to_chosen_author[self.language].format(
                    voter_display=voter_display,
                    chosen_author_display=chosen_author_display)
            msg.append(r_msg)
        msg = '\n'.join(msg)
        return build_text_block(msg)

    def build_scores_block(self):
        msg = []
        for r in self.game.results:
            guesser_display = ut.users.user_display(r['guesser'])
            score = r['score']
            assert score >= 0
            if score == 0:
                r_msg = ut.text.guesser_zero_points[self.language].format(
                    guesser_display=guesser_display)
            elif score == 1:
                r_msg = ut.text.guesser_one_point[self.language].format(
                    guesser_display=guesser_display)
            else:
                r_msg = ut.text.guesser_points[self.language].format(
                    score=score, guesser_display=guesser_display)
            msg.append(r_msg)
        msg = '\n'.join(msg)
        return build_text_block(msg)

    def build_conclusion_msg(self):
        lg = len(self.game.frozen_guessers)
        lv = len(self.game.frozen_voters)
        lw = len(self.game.winners)
        if lg == 0:
            return ut.text.no_one_submitted_an_answer[self.language]
        elif lg == 1:
            g = ut.users.user_display(list(self.game.frozen_guessers)[0])
            res = ut.text.thanks_for_your_answer[self.language].format(
                guesser_display=g)
            return res
        elif lv == 0:
            return ut.text.no_one_voted[self.language]
        elif lv == 1:
            r = self.game.results[0]
            g = ut.users.user_display(r['guesser'])
            ca = r['chosen_author']
            if ca == 'Truth':
                res = ut.text.congrats[self.language].format(
                    guesser_display=g)
                return res
            res = ut.text.too_bad[self.language].format(
                guesser_display=g,
                chosen_author_display=ut.users.user_display(ca))
            return res
        elif self.game.max_score == 0:
            return ut.text.no_points[self.language]
        elif lw == lv:
            return ut.text.draw[self.language]
        elif lw == 1:
            w = ut.users.user_display(self.game.winners[0])
            return ut.text.is_the_winner[self.language].format(
                winner_display=w)
        elif lw > 1:
            ws = [ut.users.user_display(w) for w in self.game.winners]
            res = ', '.join(ws[:-1])
            res += f' {ut.text.and_[self.language]} {ws[-1]}'
            res = ut.text.are_the_winners[self.language].format(
                winners_display_comma_final_and=res)
            return res

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
