describe('main', () => {
  it('main', () => {
    cy.get_conf().then((conf) => {
      cy.get_channel_id('english_exception_slash_command_max_this_running').then((channel_id) => {
        const tag1 = Cypress._.random(100000, 999999)
        const tag2 = Cypress._.random(100000, 999999)

        cy.login_from_user_index(conf, 0)
        cy.go_to_channel_from_channel_id(conf, channel_id)

        cy.create_fake_running_game(tag1, 0)
        cy.create_fake_running_game(tag2, 0)

        cy.slash_freestyle('tag')
        cy.contains("Vous êtes déjà le créateur de 2 parties en cours. C'est le nombre maximal autorisé")

        cy.mark_game_as_success(tag1)
        cy.mark_game_as_success(tag2)
      })
    })
  })
})