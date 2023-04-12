describe('main', () => {
  it('main', () => {
    cy.get_conf().then((conf) => {
      cy.get_channel_id('english_setup_french').then((channel_id) => {
        const tag = Cypress._.random(100000, 999999)
        cy.login_from_user_index(conf, 0)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.slash_automatic(tag)
        cy.contains('Shuffle').click()
        cy.submit_view()
        cy.contains(`${tag}: Automatic game set up by @A0!`)
        cy.contains(`${tag}: Guess`)
      })
    })
  })
})
