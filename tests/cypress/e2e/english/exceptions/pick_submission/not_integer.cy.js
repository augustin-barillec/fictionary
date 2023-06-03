describe('main', () => {
  it('main', () => {
    cy.get_conf().then((conf) => {
      cy.get_channel_id('english_exception_pick_submission_not_integer').then((channel_id) => {
        const tag = Cypress._.random(100000, 999999)
        cy.login_from_user_index(conf, 0)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.slash_automatic(tag)
        cy.get('[placeholder*="between"]').click().type('toto {enter}')
        cy.contains(`${tag}: The input provided must be an integer.`)
      })
    })
  })
})