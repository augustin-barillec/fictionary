describe('main', () => {
  it('main', () => {
    cy.get_conf().then((conf) => {
      cy.get_channel_id('ending_thanks').then((channel_id) => {
        const tag = Cypress._.random(100000, 999999)

        cy.login_from_user_index(conf, 0)
        cy.login_from_user_index(conf, 1)

        cy.login_from_user_index(conf, 0)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.organize_freestyle_game(tag, 'question', 'truth')

        cy.login_from_user_index(conf, 1)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.guess(tag, 'g1')

        cy.wait(30000)

        cy.contains(`${tag}: Freestyle game set up by @augustin!`)
        cy.contains(`${tag}: question`)
        cy.contains(`${tag}: • Truth: truth`)
        cy.contains(`${tag}: • @augustin1: g1`)
        cy.contains(`${tag}: Thanks for your guess, @augustin1!`)
      })
    })
  })
})