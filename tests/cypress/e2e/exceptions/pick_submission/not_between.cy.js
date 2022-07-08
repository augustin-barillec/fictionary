describe('main', () => {

  it('main', () => {

    cy.get_conf().then((conf) => {
      cy.get_channel_id('exception_pick_submission_not_between').then((channel_id) => {
        const tag = Cypress._.random(100000, 999999)
        cy.login_from_user_index(conf, 0)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.slash_english(tag)
        cy.get('[placeholder*="Between"]').click().type('550 {enter}')
        cy.contains(`${tag}: 550 is not between 1 and 3.`)
      })
    })
  })
})