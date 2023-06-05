ENGLISH = 'English'
FRENCH = 'French'
###############################################################################
# help
is_an_application = {
    ENGLISH: ("Fictionary is an app to play fictionary on Slack. "
              "More information is available on "
              "the app's <{home_url}|website>."),
    FRENCH: ("Fictionary est une application permettant de jouer au jeu "
             "du dictionnaire sur Slack. Plus d'informations "
             "sont disponibles sur le <{home_url}|site> de l'application.")
}
###############################################################################
# slack
new_message = {
    ENGLISH: "New message",
    FRENCH: "Nouveau message"
}

message_updated = {
    ENGLISH: "Message updated",
    FRENCH: "Message mis à jour"
}

you_can_now_vote = {
    ENGLISH: "Hey {user_display}, you can now vote in the Fictionary game "
             "created by {organizer_display}!",
    FRENCH: "Hé {user_display}, vous pouvez maintenant voter dans la partie "
            "de Fictionary créée par {organizer_display} !"
}

game_is_over = {
    ENGLISH: "The Fictionary game created by {organizer_display} is over.",
    FRENCH: "La partie de Fictionary créée par {organizer_display} "
            "est terminée."
}
###############################################################################
# blocks
time_left_to_answer = {
    ENGLISH: "Time left to answer: {time_display}",
    FRENCH: "Temps restant pour répondre : {time_display}"
}

time_left_to_vote = {
    ENGLISH: "Time left to vote: {time_display}",
    FRENCH: "Temps restant pour voter : {time_display}"
}

question_and_answer_written_by = {
    ENGLISH: "Question and answer written by {organizer_display}!",
    FRENCH: "Question et réponse écrites par {organizer_display} !"
}

question_chosen_by = {
    ENGLISH: "Question chosen by {organizer_display}!",
    FRENCH: "Question choisie par {organizer_display} !"
}

loading_the_game = {
    ENGLISH: "Loading the game...",
    FRENCH: "Chargement du jeu..."
}

loading_the_voting_stage = {
    ENGLISH: "Loading the voting stage...",
    FRENCH: "Chargement de l'étape de vote..."
}

loading_the_results = {
    ENGLISH: "Loading the results... :drum_with_drumsticks:",
    FRENCH: "Chargement des résultats... :drum_with_drumsticks:"
}

answer_verb = {
    ENGLISH: "Answer",
    FRENCH: "Répondre"
}

vote = {
    ENGLISH: "Vote",
    FRENCH: "Voter"
}

remaining_spots = {
    ENGLISH: "Remaining spots: {nb}",
    FRENCH: "Places restantes : {nb}"
}

eligible_to_vote = {
    ENGLISH: "Players eligible to vote: {user_displays}",
    FRENCH: "Joueurs pouvant voter : {user_displays}"
}

all_players_have_voted = {
    ENGLISH: "All players have voted!",
    FRENCH: "Tout les joueurs ont voté !"
}

players = {
    ENGLISH: "Players: {user_displays}",
    FRENCH: "Joueurs : {user_displays}"
}

no_one_has_answered_yet = {
    ENGLISH: "No one has answered yet.",
    FRENCH: "Personne n'a encore répondu."
}

players_who_voted = {
    ENGLISH: "Players who voted: {user_displays}",
    FRENCH: "Joueurs ayant voté : {user_displays}"
}

no_one_has_voted_yet = {
    ENGLISH: "No one has voted yet.",
    FRENCH: "Personne n'a encore voté."
}

answers = {
    ENGLISH: "Answers:",
    FRENCH: "Réponses :"
}

index_proposal = {
    ENGLISH: "{index}) {proposal}",
    FRENCH: "{index}) {proposal}"
}


game_answer_truth = {
    ENGLISH: "• Game's answer: {truth}",
    FRENCH: "• Réponse du jeu : {truth}"
}

game_answer_index_truth = {
    ENGLISH: "• Game's answer: {index}) {truth}",
    FRENCH: "• Réponse du jeu : {index}) {truth}"
}

guesser_index_guess = {
    ENGLISH: "• {guesser_display}: {index}) {guess}",
    FRENCH: "• {guesser_display} : {index}) {guess}"
}

guesser_guess = {
    ENGLISH: "• {guesser_display}: {guess}",
    FRENCH: "• {guesser_display} : {guess}"
}

voter_to_game_answer = {
    ENGLISH: "• {voter_display} -> Game's answer",
    FRENCH: "• {voter_display} -> Réponse du jeu"
}

voter_to_chosen_author = {
    ENGLISH: "• {voter_display} -> {chosen_author_display}",
    FRENCH: "• {voter_display} -> {chosen_author_display}",
}

guesser_zero_points = {
    ENGLISH: "• {guesser_display}: 0 points",
    FRENCH: "• {guesser_display} : 0 point"
}

guesser_one_point = {
    ENGLISH: "• {guesser_display}: 1 point",
    FRENCH: "• {guesser_display} : 1 point"
}

guesser_points = {
    ENGLISH: "• {guesser_display}: {score} points",
    FRENCH: "• {guesser_display} : {score} points"
}

no_one_answered = {
    ENGLISH: "No one answered. :sob:",
    FRENCH: "Personne n'a répondu. :sob:"
}

thanks_for_your_answer = {
    ENGLISH: "Thanks for your answer, {guesser_display}!",
    FRENCH: "Merci pour votre réponse, {guesser_display} !"
}

no_one_voted = {
    ENGLISH: "No one voted. :sob:",
    FRENCH: "Personne n'a voté. :sob:"
}

congrats = {
    ENGLISH: "Congrats {guesser_display}, "
             "you voted for the game's answer! :v:",
    FRENCH: "Bravo {guesser_display}, "
            "vous avez voté pour la réponse du jeu ! :v:"
}

too_bad = {
    ENGLISH: "Too bad {guesser_display}, you voted for "
             "{chosen_author_display}'s answer. :grimacing:",
    FRENCH: "Dommage {guesser_display}, vous avez voté pour la réponse "
            "de {chosen_author_display}. :grimacing:"
}

no_points = {
    ENGLISH: "No points were scored!",
    FRENCH: "Aucun point n'a été marqué !"
}

draw = {
    ENGLISH: "It's a draw! :scales:",
    FRENCH: "Match nul ! :scales:"
}

is_the_winner = {
    ENGLISH: "{winner_display} is the winner! :first_place_medal:",
    FRENCH: "{winner_display} remporte la partie ! :first_place_medal:"
}

and_ = {
    ENGLISH: "and",
    FRENCH: "et"
}

are_the_winners = {
    ENGLISH: "{winners_display_comma_final_and} are the winners! :clap:",
    FRENCH: "Les gagnants sont {winners_display_comma_final_and} ! :clap:"
}
###############################################################################
# views
close = {
    ENGLISH: "Close",
    FRENCH: "Fermer"
}

submit = {
    ENGLISH: "Submit",
    FRENCH: "Soumettre"
}

cancel = {
    ENGLISH: "Cancel",
    FRENCH: "Annuler"
}

create_a_game = {
    ENGLISH: "Create a game",
    FRENCH: "Créer une partie"
}

question = {
    ENGLISH: "Question",
    FRENCH: "Question"
}

answer_noun = {
    ENGLISH: "Answer",
    FRENCH: "Réponse"
}

questions_are_visible_here = {
    ENGLISH: "Questions are visible here:",
    FRENCH: "Les questions sont visibles ici :"
}

questions = {
    ENGLISH: "Questions",
    FRENCH: "Questions"
}

pick_a_question_number = {
    ENGLISH: "Pick a question number",
    FRENCH: "Choisir un numéro de question"
}

between_1_and_N = {
    ENGLISH: "between 1 and {N}",
    FRENCH: "entre 1 et {N}"
}

or_ = {
    ENGLISH: "*Or*",
    FRENCH: "*Ou*"
}

draw_a_question_at_random = {
    ENGLISH: "Draw a question at random",
    FRENCH: "Tirer une question au hasard"
}

question_n_selected = {
    ENGLISH: "Question *{n}* selected:",
    FRENCH: "Question *{n}* sélectionnée :"
}

your_answer = {
    ENGLISH: "Your answer",
    FRENCH: "Votre réponse"
}

write_something = {
    ENGLISH: "Write something",
    FRENCH: "Écrire quelque chose"
}

your_guess_index_guess = {
    ENGLISH: "Your answer: {index}) {guess}",
    FRENCH: "Votre réponse : {index}) {guess}"
}

your_vote = {
    ENGLISH: "Your vote",
    FRENCH: "Votre vote"
}

select_an_item = {
    ENGLISH: "Select an item",
    FRENCH: "Sélectionner un élément"
}

voting_options = {
    ENGLISH: "Voting options:",
    FRENCH: "Options de vote :"
}
###############################################################################
# exceptions
its_number_is_visible = {
    ENGLISH: ("Its number is visible on the web page of the question "
              "<{questions_url}|bank>."),
    FRENCH: ("Son numéro est visible sur la page web de la "
             "<{questions_url}|banque> de questions.")
}

there_are_already_n_games_in_progress = {
    ENGLISH: "There are already {n} games in progress.",
    FRENCH: "Il y a déjà {n} parties en cours."
}

this_is_the_maximum_number_allowed = {
    ENGLISH: "This is the maximum allowed number.",
    FRENCH: "C'est le nombre maximal autorisé."
}

you_are_already_the_creator_of_1_game_in_progress = {
    ENGLISH: "You are already the creator of 1 game in progress.",
    FRENCH: "Vous êtes déjà le créateur d'1 partie en cours."
}

you_are_already_the_organizer_of_n_games_in_progress = {
    ENGLISH: "You are already the creator of {n} running games.",
    FRENCH: "Vous êtes déjà le créateur de {n} parties en cours."
}

this_game_is_deactivated = {
    ENGLISH: "This game is deactivated.",
    FRENCH: "Cette partie est désactivée."
}

is_not_in_the_conversation = {
    ENGLISH: "Fictionary is not in the conversation.",
    FRENCH: "L'application Fictionary n'est pas dans la conversation."
}

parameter_must_be_one_of = {
    ENGLISH: "The command parameter must be one "
             "of freestyle, automatic or help.",
    FRENCH: "Le paramètre de la commande doit être l'un des suivants : "
            "freestyle, automatic ou help."
}

time_limit_for_answering_has_passed = {
    ENGLISH: ("Your answer: {guess}\n\nIt will not be taken into account "
              "because the time limit for answering has passed."),
    FRENCH: ("Votre réponse : {guess}\n\nElle ne sera pas prise en compte "
             "car la limite de temps pour répondre est passée.")
}

already_max_players = {
    ENGLISH: ("Your answer: {guess}\n\n"
              "It will not be taken into account "
              "because there are already "
              "{max_guessers_per_game} players who answered. "
              "This is the maximum allowed number for a game."),
    FRENCH: ("Votre réponse : {guess}\n\n"
             "Elle ne sera pas prise en compte "
             "car il y a déjà {max_guessers_per_game} "
             "joueurs qui ont répondu. "
             "C'est le nombre maximal autorisé par partie.")
}

time_limit_for_voting_has_passed = {
    ENGLISH: ("Your vote: answer {vote}.\n\n"
              "It will not be taken into account "
              "because the time limit for voting has passed."),
    FRENCH: ("Votre vote : réponse {vote}. \n\n" 
             "Il ne sera pas pris en compte "
             "car la limite de temps pour voter est passée.")
}

input_must_be_a_integer = {
    ENGLISH: "The input provided must be an integer.",
    FRENCH: "L'entrée renseignée doit être un entier."
}

not_between = {
    ENGLISH: "The entered integer must be between 1 and {max_number}.",
    FRENCH: "L'entier renseigné doit être compris entre 1 et {max_number}."
}

since_you_wrote = {
    ENGLISH: "Since you wrote the question and the answer for this game, "
             "you cannot participate in it.",
    FRENCH: "Comme vous avez écrit la question et la réponse de cette partie, "
            "vous ne pouvez pas y participer."
}

you_have_already_answered = {
    ENGLISH: "You have already answered.",
    FRENCH: "Vous avez déjà répondu."
}

only_players_who_answered_can_vote = {
    ENGLISH: "Only players who answered can vote.",
    FRENCH: "Seuls les joueurs ayant répondu peuvent voter."
}

you_have_already_voted = {
    ENGLISH: "You have already voted.",
    FRENCH: "Vous avez déjà voté."
}
###############################################################################
# time
time_display = {
    ENGLISH: "{minutes}min {seconds}s",
    FRENCH: "{minutes}min {seconds}s"
}
