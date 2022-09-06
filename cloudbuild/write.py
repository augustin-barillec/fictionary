from utils.writers import RunTestsWriter


def has_duplicates(list_):
    return len(set(list_)) < len(list_)


no_parallelizable_sources = [
    'exceptions/setup_submission/max_running.cy.js',
    'exceptions/slash_command/max_running.cy.js',
    'small.cy.js'
]
parallelizable_sources = [
    'endings/bravo.cy.js',
    'endings/hey.cy.js',
    'endings/no_guesses.cy.js',
    'endings/no_votes.cy.js',
    'endings/thanks.cy.js',
    'endings/well.cy.js',
    'endings/winner.cy.js',
    'endings/winners.cy.js',
    'endings/zero.cy.js',
    'exceptions/game_dead/open_view.cy.js',
    'exceptions/game_dead/update_view.cy.js',
    'exceptions/game_dead/view_response.cy.js',
    'exceptions/guess_click/already_guessed.cy.js',
    'exceptions/guess_click/organizer.cy.js',
    'exceptions/guess_submission/max_these_guessers.cy.js',
    'exceptions/guess_submission/no_time_left.cy.js',
    'exceptions/pick_submission/not_between.cy.js',
    'exceptions/pick_submission/not_integer.cy.js',
    'exceptions/setup_submission/max_this_running.cy.js',
    'exceptions/slash_command/invalid_parameter.cy.js',
    'exceptions/slash_command/max_this_running.cy.js',
    'exceptions/slash_command/not_invited.cy.js',
    'exceptions/vote_click/already_voted.cy.js',
    'exceptions/vote_click/not_a_potential_voter.cy.js',
    'exceptions/vote_submission/no_time_left.cy.js',
    'setups/english.cy.js',
    'setups/freestyle.cy.js',
    'setups/french.cy.js',
    'transitions/guess_full_time.cy.js',
    'transitions/guess_shorten_time.cy.js',
    'transitions/vote_full_time.cy.js',
    'transitions/vote_shorten_time.cy.js',
    'help.cy.js',
    'special_characters.cy.js'
]

no_parallelizable_sources = []
parallelizable_sources = [
    'endings/hey.cy.js',
    'endings/no_votes.cy.js',
    'endings/thanks.cy.js',
    'endings/winners.cy.js',
    'endings/zero.cy.js',
    'exceptions/pick_submission/not_between.cy.js',
    'exceptions/vote_click/already_voted.cy.js',
    'exceptions/vote_click/not_a_potential_voter.cy.js',
    'exceptions/vote_submission/no_time_left.cy.js',
    'transitions/guess_full_time.cy.js'
]

assert not has_duplicates(no_parallelizable_sources + parallelizable_sources)

run_tests_writer = RunTestsWriter(
    no_parallelizable_sources=no_parallelizable_sources,
    parallelizable_sources=parallelizable_sources,
    nb_batches=4)

run_tests_writer.write()
