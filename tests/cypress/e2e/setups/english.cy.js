describe('main', () => {
  it('main', () => {
    cy.get_conf().then((conf) => {
      cy.get_channel_id('setup_english').then((channel_id) => {
        const tag = Cypress._.random(100000, 999999)
        cy.login_from_user_index(conf, 0)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.slash_english(tag)
        cy.contains('English questions are visible here:')
        cy.get('[placeholder*="Between"]').click().type('1 {enter}')
        cy.contains('Question 1 selected:')
        cy.close_setup_view()
        cy.wait(5000)
        cy.contains(`${tag}: Automatic game set up by @augustin!`)
        cy.contains(`${tag}: What is 1+1 ?`)
        cy.contains(`${tag}: Guess`)
      })
    })
  })
})
