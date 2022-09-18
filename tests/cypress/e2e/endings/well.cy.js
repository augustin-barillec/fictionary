describe('main', () => {

  it('main', () => {

    cy.get_conf().then((conf) => {
      cy.get_channel_id('ending_well').then((channel_id) => {
        const tag = Cypress._.random(100000, 999999)

        cy.login_from_user_index(conf, 0)
        cy.login_from_user_index(conf, 1)
        cy.login_from_user_index(conf, 2)

        cy.login_from_user_index(conf, 0)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.organize_freestyle_game(tag, 'question', 'truth')

        cy.login_from_user_index(conf, 1)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.guess(tag, 'g1')

        cy.login_from_user_index(conf, 2)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.guess(tag, 'g2')

        cy.login_from_user_index(conf, 1)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.vote(tag, '0')

        cy.login_from_user_index(conf, 2)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.vote(tag, '0')

        cy.contains(`${tag}: Freestyle game set up by @augustin!`)
        cy.contains(`${tag}: question`)
        cy.contains(`${tag}: • Truth: 3) truth`)
        cy.contains(`${tag}: • @augustin1: 1) g1`)
        cy.contains(`${tag}: • @augustin2: 2) g2`)
        cy.contains(`${tag}: • @augustin1 -> @augustin2`)
        cy.contains(`${tag}: • @augustin2 -> @augustin1`)
        cy.contains(`${tag}: • @augustin1: 2 points`)
        cy.contains(`${tag}: • @augustin2: 2 points`)
        cy.contains(`${tag}: Well, it's a draw!`)
      })
    })
  })
})