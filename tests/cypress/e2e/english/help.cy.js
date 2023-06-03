describe('main', () => {
  it('main', () => {
    cy.get_conf().then((conf) => {
      cy.get_channel_id('english_help').then((channel_id) => {
        const tag = Cypress._.random(100000, 999999)
        cy.login_from_user_index(conf, 0)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.create_fake_running_game(tag, 0)
        cy.slash_help('tag')
        cy.contains("Fictionary is an app designed to play fictionary on Slack. More information is available on the app's website.")
        cy.mark_game_as_success(tag)
      })
    })
  })
})
