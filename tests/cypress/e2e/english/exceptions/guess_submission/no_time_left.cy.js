describe('main', () => {
  it('main', () => {
    cy.get_conf().then((conf) => {
      cy.get_channel_id('english_exception_guess_submission_no_time_left').then((channel_id) => {
        const tag = Cypress._.random(100000, 999999)

        cy.login_from_user_index(conf, 0)
        cy.login_from_user_index(conf, 1)

        cy.login_from_user_index(conf, 0)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.organize_freestyle_game(tag, 'question', 'truth')

        cy.login_from_user_index(conf, 1)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.guess_click_english(tag)
        cy.guess_type('g1')
        cy.wait(20000)
        cy.submit_view()

        cy.contains(`${tag}: Your answer: g1`)
        cy.contains(`${tag}: It will not be taken into account because the time limit for answering has passed.`)
      })
    })
  })
})
