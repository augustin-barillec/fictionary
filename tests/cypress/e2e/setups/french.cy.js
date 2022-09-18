describe('main', () => {
  it('main', () => {
    cy.get_conf().then((conf) => {
      cy.get_channel_id('setup_french').then((channel_id) => {
        const tag = Cypress._.random(100000, 999999)
        cy.login_from_user_index(conf, 0)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.slash_french(tag)
        cy.contains('Shuffle').click()
        cy.submit_view()
        cy.contains(`${tag}: Automatic game set up by @augustin!`)
        cy.contains(`${tag}: Guess`)
      })
    })
  })
})
