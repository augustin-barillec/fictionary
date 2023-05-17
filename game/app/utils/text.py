ENGLISH = 'English'
FRENCH = 'French'
###############################################################################
This_is_an_app_for_Slack = {
    ENGLISH: ('Fictionary is an application for Slack to play fictionary. '
              'All information is available <{home_url}|here.>'),
    FRENCH: ('Fictionary est une application permettant de jouer au jeu '
             'du dictionnaire sur Slack. Toutes les informations sont '
             'disponibles <{home_url}|ici.>')
}
###############################################################################
you_can_now_vote = {
    ENGLISH: 'Hey {user_display}, you can now vote in the Fictionary game '
             'created by {organizer_display}.',
    FRENCH: 'Hé {user_display}, vous pouvez maintenant voter dans la partie '
            'de Fictionary créée par {organizer_display}.'
}

game_is_over = {
    ENGLISH: 'The Fictionary game created by {organizer_display} is over.',
    FRENCH: 'La partie de Fictionary créée par {organizer_display} '
            'est terminée.'
}
###############################################################################
Time_left_to_guess = {
    ENGLISH: 'Time left to answer: {time_display}',
    FRENCH: 'Temps restant pour répondre : {time_display}'
}

Time_left_to_vote = {
    ENGLISH: 'Time left to vote: {time_display}',
    FRENCH: 'Temps restant pour voter : {time_display}'
}

Freestyle_game_set_up_by = {
    ENGLISH: 'Question and answer written by {organizer_display}.',
    FRENCH: 'Question et réponse écrites par {organizer_display}.'
}

Automatic_game_set_up_by = {
    ENGLISH: 'Question selected by {organizer_display}.',
    FRENCH: 'Question choisie par {organizer_display}.'
}

Preparing_guess_stage = {
    ENGLISH: 'Setting up the game...',
    FRENCH: 'Préparation du jeu...'
}

Preparing_vote_stage = {
    ENGLISH: 'Setting up the voting stage...',
    FRENCH: "Préparation de l'étape de vote..."
}

Computing_results = {
    ENGLISH: 'Computing results... :drum_with_drumsticks:',
    FRENCH: 'Calcul des résultats... :drum_with_drumsticks:'
}

Guess = {
    ENGLISH: 'Answer',
    FRENCH: 'Répondre'
}

Vote = {
    ENGLISH: 'Vote',
    FRENCH: 'Voter'
}

Potential_guessers = {
    ENGLISH: 'Remaining spots: {nb}',
    FRENCH: 'Places restantes : {nb}'
}

Potential_voters = {
    ENGLISH: 'Players eligible to vote: {user_displays}',
    FRENCH: 'Joueurs pouvant voter : {user_displays}'
}

Everyone_has_voted = {
    ENGLISH: 'Everyone has voted.',
    FRENCH: 'Tout le monde a voté.'
}

Guessers = {
    ENGLISH: 'Players who proposed an answer: {user_displays}',
    FRENCH: 'Joueurs ayant proposé une réponse : {user_displays}'
}

No_one_has_guessed_yet = {
    ENGLISH: 'No one has submitted an answer yet.',
    FRENCH: "Personne n'a encore proposé de réponse."
}

Voters = {
    ENGLISH: 'Players who voted: {user_displays}',
    FRENCH: 'Joueurs ayant voté : {user_displays}'
}

No_one_has_voted_yet = {
    ENGLISH: 'No one has voted yet.',
    FRENCH: "Personne n'a encore voté."
}

Proposals = {
    ENGLISH: 'Proposals:',
    FRENCH: 'Propositions :'
}

index_proposal = {
    ENGLISH: '{index}) {proposal}',
    FRENCH: '{index}) {proposal}'
}

Your_guess_index_guess = {
    ENGLISH: 'Your answer: {index}) {guess}',
    FRENCH: 'Votre réponse : {index}) {guess}'
}

Truth_truth = {
    ENGLISH: "• Game's answer: {truth}",
    FRENCH: '• Réponse du jeu : {truth}'
}

Truth_index_truth = {
    ENGLISH: "• Game's answer: {index}) {truth}",
    FRENCH: '• Réponse du jeu : {index}) {truth}'
}

guesser_index_guess = {
    ENGLISH: '• {guesser_display}: {index}) {guess}',
    FRENCH: '• {guesser_display} : {index}) {guess}'
}

guesser_guess = {
    ENGLISH: '• {guesser_display}: {guess}',
    FRENCH: '• {guesser_display} : {guess}'
}

voter_to_truth = {
    ENGLISH: "• {voter_display} -> Game's answer",
    FRENCH: '• {voter_display} -> Réponse du jeu'
}

voter_to_chosen_author = {
    ENGLISH: '• {voter_display} -> {chosen_author_display}',
    FRENCH: '• {voter_display} -> {chosen_author_display}',
}

guesser_zero_points = {
    ENGLISH: '• {guesser_display}: 0 points',
    FRENCH: '• {guesser_display} : 0 point'
}

guesser_one_point = {
    ENGLISH: '• {guesser_display}: 1 point',
    FRENCH: '• {guesser_display} : 1 point'
}

guesser_points = {
    ENGLISH: '• {guesser_display}: {score} points',
    FRENCH: '• {guesser_display} : {score} points'
}

No_one_played_this_game = {
    ENGLISH: 'No one has submitted an answer. :sob:',
    FRENCH: "Personne n'a proposé de réponse. :sob:"
}

Thanks_for_your_guess = {
    ENGLISH: 'Thanks for your proposal, {guesser_display}.',
    FRENCH: 'Merci pour votre proposition, {guesser_display}.'
}

No_one_voted = {
    ENGLISH: 'No one voted. :sob:',
    FRENCH: "Personne n'a voté. :sob:"
}

Bravo_you_found_the_truth = {
    ENGLISH: 'Well done {guesser_display}, '
             "you have voted for the game's answer! :v:",
    FRENCH: 'Bravo {guesser_display}, '
            'vous avez voté pour la réponse du jeu ! :v:'
}

Hey_at_least_you_voted = {
    ENGLISH: "Too bad {guesser_display}, you voted for "
             "{chosen_author_display}'s answer. :grimacing:",
    FRENCH: 'Dommage {guesser_display}, vous avez voté pour la réponse '
            'de {chosen_author_display}. :grimacing:'
}

Zero_points_scored = {
    ENGLISH: 'No points have been scored.',
    FRENCH: "Aucun point n'a été marqué."
}

Well_its_a_draw = {
    ENGLISH: "Well, it's a draw. :scales:",
    FRENCH: "Et bien, c'est un match nul. :scales:"
}

And_the_winner_is = {
    ENGLISH: 'And the winner is {winner_display}! :first_place_medal:',
    FRENCH: '{winner_display} remporte la partie ! :first_place_medal:'
}

and_ = {
    ENGLISH: 'and',
    FRENCH: 'et'
}

And_the_winners_are = {
    ENGLISH: 'And the winners are {winners_display_comma_final_and}! :clap:',
    FRENCH: 'Et les gagnants sont {winners_display_comma_final_and} ! :clap:'
}
###############################################################################
Close = {
    ENGLISH: 'Close',
    FRENCH: 'Fermer'
}

Submit = {
    ENGLISH: 'Submit',
    FRENCH: 'Soumettre'
}

Cancel = {
    ENGLISH: 'Cancel',
    FRENCH: 'Annuler'
}

Set_up_a_game = {
    ENGLISH: 'Set up a game',
    FRENCH: 'Créer une partie'
}

Question = {
    ENGLISH: 'Question',
    FRENCH: 'Question'
}

Answer = {
    ENGLISH: 'Answer',
    FRENCH: 'Réponse'
}

Questions_are_visible_here = {
    ENGLISH: 'Questions are visible here:',
    FRENCH: 'Les questions sont visibles ici :'
}

Questions = {
    ENGLISH: 'Questions',
    FRENCH: 'Questions'
}

Pick_a_question_number = {
    ENGLISH: 'Pick up a question number',
    FRENCH: 'Choisir un numéro de question'
}

Between_1_and_N = {
    ENGLISH: 'Between 1 and {N}',
    FRENCH: 'Entre 1 et {N}'
}

Or = {
    ENGLISH: '*Or*',
    FRENCH: '*Ou*'
}

Shuffle = {
    ENGLISH: 'Draw a question at random',
    FRENCH: 'Tirer une question au hasard'
}

Question_n_selected = {
    ENGLISH: 'Question *{n}* selected:',
    FRENCH: 'Question *{n}* sélectionnée :'
}

Your_guess = {
    ENGLISH: 'Your answer',
    FRENCH: 'Votre réponse'
}

Write_something = {
    ENGLISH: 'Write something',
    FRENCH: 'Écrire quelque chose'
}

Your_vote = {
    ENGLISH: 'Your vote',
    FRENCH: 'Votre vote'
}

Select_an_item = {
    ENGLISH: 'Select an item',
    FRENCH: 'Sélectionner un élément'
}

Voting_options = {
    ENGLISH: 'Voting options:',
    FRENCH: 'Options de vote :'
}
###############################################################################
There_is_already_1_running_game = {
    ENGLISH: 'There is already 1 game in progress.',
    FRENCH: 'Il y a déjà 1 partie en cours.'
}

There_are_already_n_running_games = {
    ENGLISH: 'There are already {n} games in progress.',
    FRENCH: 'Il y a déjà {n} parties en cours.'
}

This_is_the_maximum_number_allowed = {
    ENGLISH: 'This is the maximum allowed number.',
    FRENCH: "C'est le nombre maximal autorisé."
}

You_are_already_the_organizer_of_1_running_game = {
    ENGLISH: 'You are already the creator of one game in progress.',
    FRENCH: "Vous êtes déjà le créateur d'une partie en cours."
}

You_are_already_the_organizer_of_n_running_games = {
    ENGLISH: 'You are already the creator of {n} running games.',
    FRENCH: "Vous êtes déjà le créateur de {n} parties en cours."
}

This_game_is_dead = {
    ENGLISH: 'This game is deactivated.',
    FRENCH: 'Cette partie est désactivée.'
}

This_app_is_not_in_the_conversation = {
    ENGLISH: 'Fictionary is not in the conversation.',
    FRENCH: "L'application Fictionary n'est pas dans la conversation."
}

Parameter_must_be_one_of = {
    ENGLISH: 'The command parameter must be one '
             'of help, freestyle or automatic.',
    FRENCH: "Le paramètre de la commande doit être l'un des suivants : "
            'help, freestyle ou automatic.'
}

guessing_deadline_has_passed = {
    ENGLISH: ('Your answer: {guess}\n\nIt will not be taken into account '
              'because the time limit for answering has passed.'),
    FRENCH: ('Votre réponse: {guess}\n\nElle ne sera pas prise en compte '
             'car la limite de temps pour répondre est passée.')
}

already_too_many_guessers = {
    ENGLISH: ('Your guess: {guess}\n\n'
              'It will not be taken into account '
              'because there are already '
              '{max_guessers_per_game} players '
              'who have submitted an answer. '
              'This is the maximum allowed number for a game.'),
    FRENCH: ('Votre réponse: {guess}\n\n'
             'Elle ne sera pas prise en compte '
             'car il y a déjà {max_guessers_per_game} '
             'joueurs qui ont proposé une réponse. '
             "C'est le nombre maximal autorisé par partie.")
}

voting_deadline_has_passed = {
    ENGLISH: ('Your vote: proposal {vote}.\n\n'
              'It will not be taken into account '
              'because the time limit for voting has passed.'),
    FRENCH: ('Votre vote pour la réponse {vote} ne sera pas pris en compte '
             'car la limite de temps pour voter est passée.')
}

Input_must_be_a_integer = {
    ENGLISH: 'The input provided must be an integer.',
    FRENCH: "L'entrée renseignée doit être un entier."
}

not_between = {
    ENGLISH: 'The entered integer must be between 1 and {max_number}.',
    FRENCH: "L'entier renseigné doit être compris entre 1 et {max_number}."
}

As_the_organizer = {
    ENGLISH: 'Since you wrote the question and answer for this game, '
             'you cannot participate in it.',
    FRENCH: 'Comme vous avez écrit la question et la réponse de cette partie, '
            'vous ne pouvez pas y participer.'
}

You_have_already_guessed = {
    ENGLISH: 'You have already submitted an answer.',
    FRENCH: 'Vous avez déjà proposé une réponse.'
}

Only_guessers_can_vote = {
    ENGLISH: 'Only players who have submitted an answer can vote.',
    FRENCH: 'Seuls les joueurs ayant proposé une réponse peuvent voter.'
}

You_have_already_voted = {
    ENGLISH: 'You have already voted.',
    FRENCH: 'Vous avez déjà voté.'
}
