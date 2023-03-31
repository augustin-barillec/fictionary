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
    res['close']['text'] = ut.text.Close[language]
    res['blocks'][0]['text']['text'] = msg
    return res


def build_setup_freestyle_view(language, id_):
    res = copy.deepcopy(setup_freestyle_view_template)
    res['callback_id'] = id_
    res['submit']['text'] = ut.text.Submit[language]
    res['close']['text'] = ut.text.Cancel[language]
    res['blocks'][0]['text']['text'] = ut.text.Set_up_a_game[language]
    res['blocks'][1]['label']['text'] = ut.text.Question[language]
    res['blocks'][2]['label']['text'] = ut.text.Answer[language]
    return res


def build_setup_automatic_view(
        language, url, max_number,
        id_, pick_block_id, shuffle_block_id,
        number, question, answer):
    res = copy.deepcopy(setup_automatic_view_template)
    res['callback_id'] = id_
    res['private_metadata'] = answer
    res['submit']['text'] = ut.text.Submit[language]
    res['close']['text'] = ut.text.Cancel[language]
    res['blocks'][0]['text']['text'] = ut.text.Set_up_a_game[language]
    res['blocks'][1]['text']['text'] = ut.text.Questions_are_visible_here[
        language] + ut.text.colon[language]
    res['blocks'][1]['accessory']['text']['text'] = ut.text.Questions[language]
    res['blocks'][1]['accessory']['url'] = url
    res['blocks'][2]['block_id'] = pick_block_id
    res['blocks'][2]['label']['text'] = ut.text.Pick_a_question_number[
        language]
    res['blocks'][2]['element']['placeholder'][
        'text'] = f'{ut.text.Between_1_and[language]} {max_number}'
    res['blocks'][3]['text']['text'] = f'*{ut.text.Or[language]}*'
    res['blocks'][4]['block_id'] = shuffle_block_id
    res['blocks'][4]['elements']['text']['text'] = ut.text.Shuffle[language]
    msg = f'{ut.text.Question[language]} *{number}*'
    msg = f'{msg} {ut.text.selected[language]}{ut.text.colon[language]}'
    res['blocks'][5]['text']['text'] = msg
    res['blocks'][6]['text']['text'] = question
    return res


def build_guess_view(language, id_, question):
    res = copy.deepcopy(guess_view_template)
    res['callback_id'] = id_
    res['submit']['text'] = ut.text.Submit[language]
    res['close']['text'] = ut.text.Cancel[language]
    res['blocks'][0]['text']['text'] = question
    res['blocks'][1]['label']['text'] = ut.text.Your_guess[language]
    res['blocks'][1]['element']['placeholder']['text'] = \
        ut.text.Write_something[language]
    return res


def build_vote_view(
        language, id_,
        own_index, own_proposal,
        votable_indexed_anonymous_proposals):
    colon = {ut.text.colon[language]}
    res = copy.deepcopy(vote_view_template)
    res['callback_id'] = id_
    res['submit']['text'] = ut.text.Submit[language]
    res['close']['text'] = ut.text.Cancel[language]
    msg = f'{ut.text.Your_guess[language]}{colon} {own_index}) {own_proposal}'
    res['blocks'][0]['text']['text'] = msg
    res['blocks'][2]['label']['text'] = ut.text.Your_vote[language]
    res['blocks'][2]['element']['placeholder']['text'] = \
        ut.text.Select_an_item[language]
    votable_proposals_msg = [f'{ut.text.Voting_options}{colon}']
    option_template = res['blocks'][2]['element']['options'][0]
    vote_options = []
    for viap in votable_indexed_anonymous_proposals:
        index = viap['index']
        proposal = viap['proposal']
        votable_proposals_msg.append(f'{index}) {proposal}')
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
