describe('main', () => {
  it('main', () => {
    cy.get_conf().then((conf) => {
      cy.get_channel_id('english_exception_setup_submission_max_this_running').then((channel_id) => {
        const tag1 = Cypress._.random(100000, 999999)
        const tag2 = Cypress._.random(100000, 999999)

        cy.login_from_user_index(conf, 0)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.slash_automatic(tag1)
        cy.get('[placeholder*="between"]').click().type('1 {enter}')

        cy.create_fake_running_game(tag2, 0)

        cy.submit_view()

        cy.contains(`${tag1}: Question:`)
        cy.contains(`${tag1}: You are already the creator of 1 game in progress. This is the maximum allowed number.`)

        cy.mark_game_as_success(tag2)
      })
    })
  })
})