import json
from copy import deepcopy
from flask import Response
from app.utils import jsons, blocks, proposals


def get_view(basename):
    return jsons.get_json('views', basename)


exception_view_template = get_view('exception.json')
setup_freestyle_view_template = get_view('setup_freestyle.json')
setup_automatic_view_template = get_view('setup_automatic.json')
guess_view_template = get_view('guess.json')
vote_view_template = get_view('vote.json')


def build_exception_view(msg):
    res = deepcopy(exception_view_template)
    res['blocks'][0]['text']['text'] = msg
    return res


def build_setup_freestyle_view(id_):
    res = deepcopy(setup_freestyle_view_template)
    res['callback_id'] = id_
    return res


def build_setup_automatic_view(
        id_, pick_block_id, shuffle_block_id,
        language, url, max_number, number, question, answer):
    res = deepcopy(setup_automatic_view_template)
    res['callback_id'] = id_
    res['private_metadata'] = answer

    res['blocks'][2]['block_id'] = pick_block_id
    res['blocks'][4]['block_id'] = shuffle_block_id

    res['blocks'][1]['text'][
        'text'] = f'{language.capitalize()} questions are visible here:'
    res['blocks'][1]['accessory']['url'] = url
    res['blocks'][5]['text']['text'] = f'Question *{number}* selected: '
    res['blocks'][6]['text']['text'] = question
    res['blocks'][2]['element']['placeholder'][
        'text'] = f'Between 1 and {max_number}'
    return res


def build_guess_view(id_, question):
    res = deepcopy(guess_view_template)
    res['callback_id'] = id_
    input_block = deepcopy(res['blocks'][0])
    question_block = blocks.build_text_block(question)
    res['blocks'] = [question_block, input_block]
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
        self.surface_id_builder = self.game.surface_id_builder
        self.proposals_browser = proposals.ProposalsBrowser(game)
        self.block_builder = blocks.BlockBuilder(game)

    def build_setup_freestyle_view(self):
        id_ = self.surface_id_builder.build_setup_freestyle_view_id()
        return build_setup_freestyle_view(id_)

    def build_setup_automatic_view(
            self, url, max_number, number, question, answer):
        id_ = self.surface_id_builder.build_setup_automatic_view_id()
        pick_block_id = self.surface_id_builder.build_pick_block_id()
        shuffle_block_id = self.surface_id_builder.build_shuffle_block_id()
        language = self.game.parameter
        return build_setup_automatic_view(
            id_, pick_block_id, shuffle_block_id,
            language, url, max_number, number, question, answer)

    def build_guess_view(self):
        id_ = self.surface_id_builder.build_guess_view_id()
        return build_guess_view(id_, self.game.question)

    def build_vote_view(self, voter):
        res = deepcopy(vote_view_template)
        res['callback_id'] = self.surface_id_builder.build_vote_view_id()
        input_block_template = res['blocks'][0]
        votable_proposals_msg = ['Voting options:']
        option_template = input_block_template['element']['options'][0]
        vote_options = []
        for viap in self.proposals_browser.\
                build_votable_indexed_anonymous_proposals(voter):
            index = viap['index']
            proposal = viap['proposal']
            votable_proposals_msg.append(f'{index}) {proposal}')
            vote_option = deepcopy(option_template)
            vote_option['text']['text'] = f'{index}'
            vote_option['value'] = f'{index}'
            vote_options.append(vote_option)
        votable_proposals_msg = '\n'.join(votable_proposals_msg)
        input_block = input_block_template
        input_block['element']['options'] = vote_options
        res['blocks'] = [
            self.block_builder.build_own_guess_block(voter),
            blocks.build_text_block(votable_proposals_msg),
            input_block]
        return res
