from utils.writers import RunTestsWriter


no_parallelizable_sources = [
    'exceptions/setup_submission/max_running.js',
    'exceptions/slash_command/max_running.js',
    'small_test.js'
]
parallelizable_sources = [
    'endings/bravo.js',
    'endings/hey.js',
    'endings/no_guesses.js',
    'endings/no_votes.js',
    'endings/thanks.js',
    'endings/well.js',
    'endings/winner.js',
    'endings/winners.js',
    'endings/zero.js',

    'transitions/guess_full.js',
    'transitions/guess_shorten.js',
    'transitions/vote_full.js',
    'transitions/vote_shorten.js',

    'exceptions/guess_click/already_guessed.js',
    'exceptions/guess_click/max_these_guessers.js',
    'exceptions/guess_click/not_a_member.js',
    'exceptions/guess_click/organizer.js',
    'exceptions/guess_submission/max_these_guessers.js',
    'exceptions/guess_submission/no_time_left.js',
    'exceptions/setup_submission/max_this_running.js',
    'exceptions/slash_command/max_this_running.js',
    'exceptions/slash_command/not_invited.js',
    'exceptions/vote_click/already_voted.js',
    'exceptions/vote_click/not_a_potential_voter.js',
    'exceptions/vote_submission/no_time_left.js',

    'special_characters.js'
]


run_tests_writer = RunTestsWriter(
    no_parallelizable_sources=no_parallelizable_sources,
    parallelizable_sources=parallelizable_sources,
    nb_batches=4)

run_tests_writer.write()
