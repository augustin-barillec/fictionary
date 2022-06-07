describe('main', () => {

  it('main', () => {

    cy.get_conf().then((conf) => {
      cy.get_channel_id('exception_slash_command_max_running').then((channel_id) => {
        cy.clean_games()

        const tag = Cypress._.random(100000, 999999)

        cy.login_from_user_index(conf, 0)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.organize_freestyle_game('', 'question', 'truth')
        cy.organize_freestyle_game('', 'question', 'truth')
        cy.organize_freestyle_game('', 'question', 'truth')
        cy.slash_command(tag)

        cy.contains(`${tag}: There are already 3 games running! This is the maximal number allowed.`)

      })
    })
  })
})
