describe('main', () => {
  it('main', () => {
    cy.get_conf().then((conf) => {
      cy.get_channel_id('french_ending_no_guesses').then((channel_id) => {
        const tag = Cypress._.random(100000, 999999)

        cy.login_from_user_index(conf, 0)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.organize_freestyle_game(tag, 'question', 'truth')

        cy.contains(`${tag}: Question et réponse écrites par @A0 !`)
        cy.contains(`${tag}: question`)
        cy.contains(`${tag}: • Réponse du jeu : truth`)
        cy.contains(`${tag}: Personne n'a proposé de réponse.`)
      })
    })
  })
})
