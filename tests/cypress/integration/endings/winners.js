describe('main', () => {

  it('main', () => {

    cy.get_conf().then((conf) => {
      cy.get_channel_id('ending_winners').then((channel_id) => {
        const tag = Cypress._.random(100000, 999999)

        cy.login_from_user_index(conf, 0)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.organize_game(tag, 'question', 'truth')

        cy.login_from_user_index(conf, 1)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.guess(tag, 'g1')

        cy.login_from_user_index(conf, 2)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.guess(tag, 'g2')

        cy.login_from_user_index(conf, 3)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.guess(tag, 'g3')

        cy.login_from_user_index(conf, 1)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.vote(tag, '0')

        cy.login_from_user_index(conf, 2)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.vote(tag, '0')

        cy.login_from_user_index(conf, 3)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.vote(tag, '2')

        cy.wait(15000)
        cy.contains(`${tag}: And the winners are @augustin1 and @augustin2!`)
      })
    })
  })
})