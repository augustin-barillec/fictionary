describe('main', () => {
  it('main', () => {
    cy.get_conf().then((conf) => {
      cy.get_channel_id('english_ending_winners').then((channel_id) => {
        const tag = Cypress._.random(100000, 999999)

        cy.login_from_user_index(conf, 0)
        cy.login_from_user_index(conf, 1)
        cy.login_from_user_index(conf, 2)
        cy.login_from_user_index(conf, 3)

        cy.login_from_user_index(conf, 0)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.organize_freestyle_game(tag, 'question', 'truth')

        cy.login_from_user_index(conf, 1)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.guess_english(tag, 'g1')

        cy.login_from_user_index(conf, 2)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.guess_english(tag, 'g2')

        cy.login_from_user_index(conf, 3)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.guess_english(tag, 'g3')

        cy.login_from_user_index(conf, 1)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.vote_english(tag, '0')

        cy.login_from_user_index(conf, 2)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.vote_english(tag, '0')

        cy.login_from_user_index(conf, 3)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.vote_english(tag, '2')

        cy.contains(`${tag}: Question and answer written by @A0!`)
        cy.contains(`${tag}: question`)
        cy.contains(`${tag}: • Game's answer: 4) truth`)
        cy.contains(`${tag}: • @A1: 1) g1`)
        cy.contains(`${tag}: • @A2: 2) g2`)
        cy.contains(`${tag}: • @A3: 3) g3`)
        cy.contains(`${tag}: • @A1 -> @A2`)
        cy.contains(`${tag}: • @A2 -> @A1`)
        cy.contains(`${tag}: • @A3 -> Truth`)
        cy.contains(`${tag}: • @A1: 2 points`)
        cy.contains(`${tag}: • @A2: 2 points`)
        cy.contains(`${tag}: • @A3: 1 point`)
        cy.contains(`${tag}: And the winners are @A1 and @A2! 👏`)
      })
    })
  })
})