describe('main', () => {
  it('main', () => {
    cy.get_conf().then((conf) => {
      cy.get_channel_id('english_setup_automatic_shuffle').then((channel_id) => {
        const tag = Cypress._.random(100000, 999999)
        cy.login_from_user_index(conf, 0)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.slash_automatic(tag)
        cy.contains('Draw a question at random').click()
        cy.submit_view()
        cy.contains(`${tag}: Question selected by @A0!`)
        cy.contains(`${tag}: Answer`)
      })
    })
  })
})
