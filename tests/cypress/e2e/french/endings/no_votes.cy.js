describe('main', () => {
  it('main', () => {
    cy.get_conf().then((conf) => {
      cy.get_channel_id('french_ending_no_votes').then((channel_id) => {
        const tag = Cypress._.random(100000, 999999)

        cy.login_from_user_index(conf, 0)
        cy.login_from_user_index(conf, 1)
        cy.login_from_user_index(conf, 2)

        cy.login_from_user_index(conf, 0)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.organize_freestyle_game(tag, 'question', 'truth')

        cy.login_from_user_index(conf, 1)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.guess_french(tag, 'g1')

        cy.login_from_user_index(conf, 2)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.guess_french(tag, 'g2')

        cy.wait(20000)

        cy.contains(`${tag}: Question et réponse écrites par @A0 !`)
        cy.contains(`${tag}: question`)
        cy.contains(`${tag}: • Réponse du jeu : 3) truth`)
        cy.contains(`${tag}: • @A1 : 1) g1`)
        cy.contains(`${tag}: • @A2 : 2) g2`)
        cy.contains(`${tag}: Personne n'a voté.`)
      })
    })
  })
})
