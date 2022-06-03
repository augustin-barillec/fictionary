describe('main', () => {

  it('main', () => {

    cy.get_conf().then((conf) => {
      cy.get_channel_id('exception_guess_click_not_a_member').then((channel_id) => {
        const tag = Cypress._.random(100000, 999999)

        cy.kick_from_channel(channel_id, 2)

        cy.login_from_user_index(conf, 0)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.organize_game(tag, 'question', 'truth')

        cy.wait(10000)
        cy.invite_to_channel(channel_id, 2)


        cy.login_from_user_index(conf, 2)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.guess_click(tag)

        cy.contains(`${tag}: You cannot guess because when the set up of this game started, you were not a member of this channel.`)
      })
    })
  })
})