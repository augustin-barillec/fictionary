describe('main', () => {
  it('main', () => {
    cy.get_conf().then((conf) => {
      cy.get_channel_id('english_exception_setup_submission_max_running').then((channel_id) => {
        const tag1 = Cypress._.random(100000, 999999)
        const tag2 = Cypress._.random(100000, 999999)
        const tag3 = Cypress._.random(100000, 999999)
        const tag4 = Cypress._.random(100000, 999999)
        const tag5 = Cypress._.random(100000, 999999)

        cy.login_from_user_index(conf, 0)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.slash_freestyle(tag1)
        cy.write_question_truth('question', 'truth')

        cy.create_fake_running_game(tag2, 0)
        cy.create_fake_running_game(tag3, 1)
        cy.create_fake_running_game(tag4, 2)
        cy.create_fake_running_game(tag5, 3)

        cy.submit_view()

        cy.contains(`${tag1}: Question: question`)
        cy.contains(`${tag1}: Answer: truth`)
        cy.contains(`${tag1}: There are already 4 games running! This is the maximal number allowed.`)

        cy.mark_game_as_success(tag2)
        cy.mark_game_as_success(tag3)
        cy.mark_game_as_success(tag4)
        cy.mark_game_as_success(tag5)
      })
    })
  })
})