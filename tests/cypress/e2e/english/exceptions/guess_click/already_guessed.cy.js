describe('main', () => {
  it('main', () => {
    cy.get_conf().then((conf) => {
      cy.get_channel_id('english_exception_guess_click_already_guessed').then((channel_id) => {
        const tag = Cypress._.random(100000, 999999)

        cy.login_from_user_index(conf, 0)
        cy.login_from_user_index(conf, 1)

        cy.login_from_user_index(conf, 0)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.organize_freestyle_game(tag, 'question', 'truth')

        cy.login_from_user_index(conf, 1)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.guess_english(tag, 'g1')
        cy.guess_click(tag)

        cy.contains(`${tag}: You have already submitted an answer.`)
      })
    })
  })
})