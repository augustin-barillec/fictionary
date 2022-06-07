describe('main', () => {

  it('main', () => {

    cy.get_conf().then((conf) => {
      cy.get_channel_id('exception_setup_submission_max_this_running').then((channel_id) => {
        const tag = Cypress._.random(100000, 999999)
        const organizer_index = 1

        cy.login_from_user_index(conf, organizer_index)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.slash_command(tag)
        cy.write_question_and_truth('question', 'truth')

        cy.create_fake_running_game(organizer_index)
        cy.create_fake_running_game(organizer_index)

        cy.close_setup_view()

        cy.contains(`${tag}: Question: question`)
        cy.contains('Answer: truth')
        cy.contains('You are already the organizer of 2 running games. This is the maximum number allowed.')
      })
    })
  })
})