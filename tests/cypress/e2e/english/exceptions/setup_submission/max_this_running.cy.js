describe('main', () => {
  it('main', () => {
    cy.get_conf().then((conf) => {
      cy.get_channel_id('english_exception_setup_submission_max_this_running').then((channel_id) => {
        const tag1 = Cypress._.random(100000, 999999)
        const tag2 = Cypress._.random(100000, 999999)
        const tag3 = Cypress._.random(100000, 999999)

        cy.login_from_user_index(conf, 0)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.slash_freestyle(tag1)
        cy.write_question_truth('question', 'truth')

        cy.create_fake_running_game(tag2, 0)
        cy.create_fake_running_game(tag3, 0)

        cy.submit_view()

        cy.contains(`${tag1}: Question: question`)
        cy.contains(`${tag1}: Answer: truth`)
        cy.contains(`${tag1}: You are already the organizer of 2 running games. This is the maximum number allowed.`)

        cy.mark_game_as_success(tag2)
        cy.mark_game_as_success(tag3)
      })
    })
  })
})