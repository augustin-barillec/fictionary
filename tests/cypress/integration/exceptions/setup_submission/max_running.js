describe('main', () => {

  it('main', () => {

    cy.get_conf().then((conf) => {
      cy.get_channel_id('exception_setup_submission_max_running').then((channel_id) => {
        cy.clean_games()

        const tag = Cypress._.random(100000, 999999)

        cy.login_from_user_index(conf, 0)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.slash_command(tag)
        cy.write_question_and_truth('question', 'truth')

        cy.create_fake_running_game(0)
        cy.create_fake_running_game(1)
        cy.create_fake_running_game(2)
        cy.create_fake_running_game(3)

        cy.close_setup_view()

        cy.contains(`${tag}: Question: question`)
        cy.contains('Answer: truth')
        cy.contains('There are already 4 games running! This is the maximal number allowed.')

      })
    })
  })
})