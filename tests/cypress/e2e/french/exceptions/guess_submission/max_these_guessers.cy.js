describe('main', () => {
  it('main', () => {
    cy.get_conf().then((conf) => {
      cy.get_channel_id('french_exception_guess_submission_max_these_guessers').then((channel_id) => {
        const tag = Cypress._.random(100000, 999999)

        cy.login_from_user_index(conf, 0)
        cy.login_from_user_index(conf, 1)

        cy.login_from_user_index(conf, 0)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.organize_freestyle_game(tag, 'question', 'truth')

        cy.login_from_user_index(conf, 1)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.guess_click_french(tag)
        cy.guess_type('g1')

        cy.create_fake_guess(tag, 2)
        cy.create_fake_guess(tag, 3)

        cy.submit_view()

        cy.contains(`${tag}: Votre réponse : g1`)
        cy.contains(`${tag}: Elle ne sera pas prise en compte car il y a déjà 2 joueurs qui ont répondu. C'est le nombre maximal autorisé par partie.`)
      })
    })
  })

