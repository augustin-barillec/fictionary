describe('main', () => {
  it('main', () => {
    cy.get_conf().then((conf) => {
      const tag = Cypress._.random(100000, 999999)
      cy.login_from_user_index(conf, 0)
      cy.organize_freestyle_game(tag, 'question', 'truth')
      cy.mark_game_as_success(tag)
    })
  })
})