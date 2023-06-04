describe('main', () => {
  it('main', () => {
    cy.get_conf().then((conf) => {
      cy.get_channel_id('french_exception_game_dead_update_view').then((channel_id) => {
        const tag = Cypress._.random(100000, 999999)
        cy.login_from_user_index(conf, 0)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.slash_automatic(tag)
        cy.get('[placeholder*="entre"]').click().type('1 {enter}')
        cy.contains(`${tag}: Cette partie est désactivée.`)
      })
    })
  })
})