describe('main', () => {
  it('main', () => {
    cy.get_conf().then((conf) => {
      cy.get_channel_id('english_exception_guess_click_organizer').then((channel_id) => {
        const tag = Cypress._.random(100000, 999999)
        cy.login_from_user_index(conf, 0)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.organize_freestyle_game(tag, 'question', 'truth')
        cy.guess_click(tag)
        cy.contains(`${tag}: Since you wrote the question and the answer for this game, you cannot participate in it.`)
      })
    })
  })
})