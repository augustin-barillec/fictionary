describe('main', () => {
  it('main', () => {
    cy.get_conf().then((conf) => {
      cy.get_channel_id('english_exception_game_dead_view_response').then((channel_id) => {
        const tag = Cypress._.random(100000, 999999)

        cy.login_from_user_index(conf, 0)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.slash_freestyle(tag)
        cy.write_question_truth('question', 'truth')

        cy.delete_game(tag)

        cy.submit_view()

        cy.contains('This game is dead!')
      })
    })
  })
})