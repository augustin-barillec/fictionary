const YAML = require('yamljs')
const project_id = Cypress.env('PROJECT_ID')

Cypress.Commands.add('run_context', (argument) => {
  cy.exec(`python context.py --project_id ${project_id} ${argument}`)
})

Cypress.Commands.add('print_conf', () => {
  cy.run_context('print_conf')
})

Cypress.Commands.add('print_channel_id', channel_name => {
  cy.run_context(`print_channel_id ${channel_name}`)
})

Cypress.Commands.add('clean_games', () => {
  cy.run_context('clean_games')
})

Cypress.Commands.add('create_fake_guesser', tag => {
  cy.run_context(`create_fake_guesser ${tag}`)
})

Cypress.Commands.add('create_fake_running_game', organizer_index => {
  cy.run_context(`create_fake_running_game ${organizer_index}`)
})

Cypress.Commands.add('kick_from_channel', (channel_id, user_index) => {
  cy.run_context(`kick_from_channel ${channel_id} ${user_index}`)
})

Cypress.Commands.add('invite_to_channel', (channel_id, user_index) => {
  cy.run_context(`invite_to_channel ${channel_id} ${user_index}`)
})

Cypress.Commands.add('get_conf', () => {
  cy.print_conf().then((result) => {
    return YAML.parse(result.stdout)
  })
})

Cypress.Commands.add('get_channel_id', channel_name => {
  cy.print_channel_id(channel_name).then((result) => {
    return result.stdout
  })
})

Cypress.Commands.add('login', (signin_url, email, password) => {
  cy.clearCookies()
  cy.visit(signin_url)
  cy.wait(1000)
  cy.visit(signin_url)
  cy.wait(1000)
  cy.get('#email').click().type(email).should('have.value', email)
  cy.get('#password').click().type(password, {log: false })
  cy.get('#signin_btn').click()
})

Cypress.Commands.add('login_from_user_index', (conf, user_index) => {
  const signin_url = conf.signin_url
  const email = conf.users[user_index].email
  const password = conf.users[user_index].password
  cy.login(signin_url, email, password)
})

Cypress.Commands.add('go_to_channel_from_channel_id', (conf, channel_id) => {
  const team_id = conf.team_id
  const url = `https://app.slack.com/client/${team_id}/${channel_id}`
  cy.visit(url)
  cy.wait(1000)
  cy.visit(url)
  cy.wait(1000)
})

Cypress.Commands.add('slash_command', (parameter, tag) => {
  cy.get('.ql-editor > p').click().clear().type(`/fictionary ${parameter} ${tag} {enter}`)
})

Cypress.Commands.add('slash_help', tag => {
  cy.slash_command('help', tag)
})

Cypress.Commands.add('slash_freestyle', tag => {
  cy.slash_command('freestyle', tag)
})

Cypress.Commands.add('slash_english', tag => {
  cy.slash_command('english', tag)
})

Cypress.Commands.add('slash_french', tag => {
  cy.slash_command('french', tag)
})

Cypress.Commands.add('write_question_truth', (question, truth) => {
  cy.get('#question-question').click().type(question).should('have.value', question)
  cy.get('#truth-truth').click().type(truth).should('have.value', truth)
})

Cypress.Commands.add('close_setup_view', () => {
  cy.get('.c-wizard_modal__footer > .c-button--primary').click()
})

Cypress.Commands.add('organize_freestyle_game', (tag, question, truth) => {
  cy.slash_freestyle(tag)
  cy.write_question_truth(question, truth)
  cy.close_setup_view()
})

Cypress.Commands.add('guess_click', tag => {
  cy.contains(`${tag}: Guess`).click()
})

Cypress.Commands.add('guess_type', guess => {
   cy.get('#guess-guess').click().type(guess).should('have.value', guess)
})

Cypress.Commands.add('guess_submit', () => {
   cy.get('.c-wizard_modal__footer > .c-button--primary').click()
})

Cypress.Commands.add('guess', (tag, guess) => {
  cy.guess_click(tag)
  cy.guess_type(guess)
  cy.guess_submit()
})

Cypress.Commands.add('vote_click', tag => {
  cy.contains(`${tag}: Vote`).click()
})

Cypress.Commands.add('vote_select', vote => {
  cy.get('#vote-vote').click()
  cy.get(`#vote-vote_option_${vote} > .c-select_options_list__option_label > .p-block-kit-select_options`).click()
})

Cypress.Commands.add('vote_submit', () => {
  cy.get('.c-wizard_modal__footer > .c-button--primary').click()
})

Cypress.Commands.add('vote', (tag, vote) => {
  cy.vote_click(tag)
  cy.vote_select(vote)
  cy.vote_submit()
})
