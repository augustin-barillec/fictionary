describe('main', () => {
  it('main', () => {
    cy.get_conf().then((conf) => {
      cy.clean_games()
      cy.login_from_user_index(conf, 0)
      cy.organize_freestyle_game('tag', 'question', 'truth')
    })
  })
})