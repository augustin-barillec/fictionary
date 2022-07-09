describe('main', () => {

  it('main', () => {

    cy.get_conf().then((conf) => {
      cy.get_channel_id('exception_vote_click_not_a_potential_voter').then((channel_id) => {
        const tag = Cypress._.random(100000, 999999)

        cy.login_from_user_index(conf, 0)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.organize_freestyle_game(tag, 'question', 'truth')

        cy.login_from_user_index(conf, 1)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.guess(tag, 'g1')

        cy.login_from_user_index(conf, 2)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.guess(tag, 'g2')

        cy.login_from_user_index(conf, 3)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.wait(20000)
        cy.vote_click(tag)

        cy.contains(`${tag}: Only guessers can vote!`)
      })
    })
  })
})
