describe('main', () => {
  it('main', () => {
    cy.get_conf().then((conf) => {
      cy.login_from_user_index(conf, 0)
      cy.slash_french('tag')
      cy.get('[placeholder*="Between"]').click().type('1 {enter}')
      cy.contains('Question 1 selected:')
    })
  })
})
