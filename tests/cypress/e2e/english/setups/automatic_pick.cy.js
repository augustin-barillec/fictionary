describe('main', () => {
  it('main', () => {
    cy.get_conf().then((conf) => {
      cy.get_channel_id('english_setup_automatic_pick').then((channel_id) => {
        const tag = Cypress._.random(100000, 999999)
        cy.login_from_user_index(conf, 0)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.slash_automatic(tag)
        cy.contains('Questions are visible here:')
        cy.get('[placeholder*="Between"]').click().type('1 {enter}')
        cy.contains('Question 1 selected:')
        cy.submit_view()
        cy.contains(`${tag}: Automatic game set up by @A0!`)
        cy.contains(`${tag}: Guess`)
      })
    })
  })
})
