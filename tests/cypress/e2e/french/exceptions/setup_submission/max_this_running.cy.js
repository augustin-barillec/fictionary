describe('main', () => {
  it('main', () => {
    cy.get_conf().then((conf) => {
      cy.get_channel_id('french_exception_setup_submission_max_this_running').then((channel_id) => {
        const tag1 = Cypress._.random(100000, 999999)
        const tag2 = Cypress._.random(100000, 999999)

        cy.login_from_user_index(conf, 0)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.slash_automatic(tag1)

        cy.create_fake_running_game(tag2, 0)

        cy.submit_view()

        cy.contains(`${tag1}: Question:`)
        cy.contains(`${tag1}: Son numéro est visible sur la page web de la banque de questions.`)
        cy.contains(`${tag1}: Vous êtes déjà le créateur d'1 partie en cours. C'est le nombre maximal autorisé.`)

        cy.mark_game_as_success(tag2)
      })
    })
  })
})
