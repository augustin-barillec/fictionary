describe('main', () => {
  it('main', () => {
    cy.get_conf().then((conf) => {
      cy.get_channel_id('english_exception_guess_submission_max_these_guessers').then((channel_id) => {
        const tag = Cypress._.random(100000, 999999)

        cy.login_from_user_index(conf, 0)
        cy.login_from_user_index(conf, 1)

        cy.login_from_user_index(conf, 0)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.organize_freestyle_game(tag, 'question', 'truth')

        cy.login_from_user_index(conf, 1)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.guess_click(tag)
        cy.guess_type('g1')

        cy.create_fake_guess(tag, 2)
        cy.create_fake_guess(tag, 3)

        cy.submit_view()

        cy.contains(`${tag}: Your guess: g1`)
        cy.contains(`${tag}: It will not be taken into account because there are already 2 guessers. This is the maximal number allowed for a game.`)
      })
    })
  })
})