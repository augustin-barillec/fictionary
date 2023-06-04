describe('main', () => {
  it('main', () => {
    cy.get_conf().then((conf) => {
      cy.get_channel_id('english_special_characters').then((channel_id) => {
        const tag = Cypress._.random(100000, 999999)

        cy.login_from_user_index(conf, 0)
        cy.login_from_user_index(conf, 1)
        cy.login_from_user_index(conf, 2)
        cy.login_from_user_index(conf, 3)

        cy.login_from_user_index(conf, 0)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.organize_freestyle_game(tag, 'question :robot_face:', 'truth 😃')

        cy.login_from_user_index(conf, 1)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.guess_french(tag, '是')

        cy.login_from_user_index(conf, 2)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.guess_french(tag, '🌍, 🍞, 🚗, 📞, 🎉')

        cy.login_from_user_index(conf, 3)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.guess_french(tag, 'g3')

        cy.login_from_user_index(conf, 1)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.vote_french(tag, '0')

        cy.login_from_user_index(conf, 2)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.vote_french(tag, '0')

        cy.login_from_user_index(conf, 3)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.vote_french(tag, '2')

        cy.wait(15000)
        cy.contains(`${tag}: La partie de Fictionary créée par @A0 est terminée.`)
      })
    })
  })
})