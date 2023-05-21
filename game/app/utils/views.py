import copy
import app.utils as ut


def get_view(basename):
    return ut.jsons.get_json('views', basename)


exception_view_template = get_view('exception.json')
setup_freestyle_view_template = get_view('setup_freestyle.json')
setup_automatic_view_template = get_view('setup_automatic.json')
guess_view_template = get_view('guess.json')
vote_view_template = get_view('vote.json')


def build_exception_view(language, msg):
    res = copy.deepcopy(exception_view_template)
    res['close']['text'] = ut.text.close[language]
    res['blocks'][0]['text']['text'] = msg
    return res


def build_setup_freestyle_view(language, id_):
    res = copy.deepcopy(setup_freestyle_view_template)
    res['callback_id'] = id_
    res['submit']['text'] = ut.text.submit[language]
    res['close']['text'] = ut.text.cancel[language]
    res['blocks'][0]['text']['text'] = ut.text.set_up_a_game[language]
    res['blocks'][1]['label']['text'] = ut.text.question[language]
    res['blocks'][1]['element']['placeholder']['text'] = \
        ut.text.Write_something[language]
    res['blocks'][2]['label']['text'] = ut.text.answer[language]
    res['blocks'][2]['element']['placeholder']['text'] = \
        ut.text.Write_something[language]
    return res


def build_setup_automatic_view(
        language, url, max_number,
        id_, pick_block_id, shuffle_block_id,
        number, question, answer):
    res = copy.deepcopy(setup_automatic_view_template)
    res['callback_id'] = id_
    res['private_metadata'] = answer
    res['submit']['text'] = ut.text.submit[language]
    res['close']['text'] = ut.text.cancel[language]
    res['blocks'][0]['text']['text'] = ut.text.set_up_a_game[language]
    res['blocks'][1]['text']['text'] = ut.text.questions_are_visible_here[
        language]
    res['blocks'][1]['accessory']['text']['text'] = ut.text.questions[language]
    res['blocks'][1]['accessory']['url'] = url
    res['blocks'][2]['block_id'] = pick_block_id
    res['blocks'][2]['label']['text'] = ut.text.pick_a_question_number[
        language]
    res['blocks'][2]['element']['placeholder'][
        'text'] = ut.text.between_1_and_N[language].format(N=max_number)
    res['blocks'][3]['text']['text'] = ut.text.or_[language]
    res['blocks'][4]['block_id'] = shuffle_block_id
    res['blocks'][4]['elements'][0]['text']['text'] = \
        ut.text.draw_a_question_at_random[language]
    res['blocks'][5]['text']['text'] = ut.text.question_n_selected[
        language].format(n=number)
    res['blocks'][6]['text']['text'] = question
    return res


def build_guess_view(language, id_, question):
    res = copy.deepcopy(guess_view_template)
    res['callback_id'] = id_
    res['submit']['text'] = ut.text.submit[language]
    res['close']['text'] = ut.text.cancel[language]
    res['blocks'][0]['text']['text'] = question
    res['blocks'][1]['label']['text'] = ut.text.your_answer[language]
    res['blocks'][1]['element']['placeholder']['text'] = \
        ut.text.write_something[language]
    return res


def build_vote_view(
        language, id_,
        own_index, own_proposal,
        votable_indexed_anonymous_proposals):
    res = copy.deepcopy(vote_view_template)
    res['callback_id'] = id_
    res['submit']['text'] = ut.text.submit[language]
    res['close']['text'] = ut.text.cancel[language]
    msg = ut.text.your_guess_index_guess[language].format(
        index=own_index, guess=own_proposal)
    res['blocks'][0]['text']['text'] = msg
    res['blocks'][2]['label']['text'] = ut.text.your_vote[language]
    res['blocks'][2]['element']['placeholder']['text'] = \
        ut.text.select_an_item[language]
    votable_proposals_msg = [ut.text.voting_options[language]]
    option_template = res['blocks'][2]['element']['options'][0]
    vote_options = []
    for viap in votable_indexed_anonymous_proposals:
        index = viap['index']
        proposal = viap['proposal']
        votable_proposals_msg.append(ut.text.index_proposal[language].format(
            index=index, proposal=proposal))
        vote_option = copy.deepcopy(option_template)
        index_str = str(index)
        vote_option['text']['text'] = index_str
        vote_option['value'] = index_str
        vote_options.append(vote_option)
    votable_proposals_msg = '\n'.join(votable_proposals_msg)
    res['blocks'][1]['text']['text'] = votable_proposals_msg
    res['blocks'][2]['element']['options'] = vote_options
    return res


def collect_setup_freestyle(setup_freestyle_view):
    values = setup_freestyle_view['state']['values']
    question = values['question']['question']['value']
    truth = values['truth']['truth']['value']
    return question, truth


def collect_setup_automatic(setup_automatic_view):
    question = setup_automatic_view['blocks'][6]['text']['text']
    truth = setup_automatic_view['private_metadata']
    return question, truth


def collect_guess(guess_view):
    values = guess_view['state']['values']
    guess = values['guess']['guess']['value']
    return guess


def collect_vote(vote_view):
    values = vote_view['state']['values']
    vote = int(values['vote']['vote']['selected_option']['value'])
    return vote


class ViewBuilder:
    def __init__(self, game):
        self.game = game
        self.language = self.game.language
        self.surface_id_builder = self.game.surface_id_builder
        self.proposals_browser = ut.proposals.ProposalsBrowser(self.game)
        self.block_builder = ut.blocks.BlockBuilder(self.game)

    def build_setup_freestyle_view(self):
        id_ = self.surface_id_builder.build_setup_freestyle_view_id()
        return build_setup_freestyle_view(self.language, id_)

    def build_setup_automatic_view(
            self, url, max_number, number, question, answer):
        language = self.language
        id_ = self.surface_id_builder.build_setup_automatic_view_id()
        pick_block_id = self.surface_id_builder.build_pick_block_id()
        shuffle_block_id = self.surface_id_builder.build_shuffle_block_id()
        return build_setup_automatic_view(
            language, url, max_number,
            id_, pick_block_id, shuffle_block_id,
            number, question, answer)

    def build_guess_view(self):
        id_ = self.surface_id_builder.build_guess_view_id()
        return build_guess_view(self.language, id_, self.game.question)

    def build_vote_view(self, voter):
        id_ = self.surface_id_builder.build_vote_view_id()
        own_index, own_proposal = \
            self.proposals_browser.build_own_indexed_guess(voter)
        viaps = self.proposals_browser.\
            build_votable_indexed_anonymous_proposals(voter)
        return build_vote_view(
            self.language, id_, own_index, own_proposal, viaps)
