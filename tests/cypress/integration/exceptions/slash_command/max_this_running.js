describe('main', () => {

  it('main', () => {

    cy.get_conf().then((conf) => {
      cy.get_channel_id('exception_slash_command_max_this_running').then((channel_id) => {
        const tag = Cypress._.random(100000, 999999)

        cy.login_from_user_index(conf, 2)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.organize_game('', 'question', 'truth')
        cy.organize_game('', 'question', 'truth')
        cy.slash_command(tag)

        cy.contains(`${tag}: You are already the organizer of 2 running games. This is the maximum number allowed.`)
      })
    })
  })
})