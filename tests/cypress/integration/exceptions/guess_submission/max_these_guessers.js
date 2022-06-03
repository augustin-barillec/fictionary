describe('main', () => {

  it('main', () => {

    cy.get_conf().then((conf) => {
      cy.get_channel_id('exception_guess_submission_max_these_guessers').then((channel_id) => {
        const tag = Cypress._.random(100000, 999999)

        cy.login_from_user_index(conf, 0)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.organize_game(tag, 'question', 'truth')

        cy.login_from_user_index(conf, 1)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.guess_click(tag)
        cy.guess_type('g1')
        cy.create_fake_guesser(tag)
        cy.create_fake_guesser(tag)
        cy.create_fake_guesser(tag)
        cy.create_fake_guesser(tag)
        cy.create_fake_guesser(tag)

        cy.guess_submit()

        cy.contains(`${tag}: Your guess: g1`)
        cy.contains('It will not be taken into account because there are already 5 guessers. This is the maximal number allowed')
      })
    })
  })
})