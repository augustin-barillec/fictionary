describe('main', () => {

  it('main', () => {

    cy.get_conf().then((conf) => {
      cy.get_channel_id('exception_pick_submission_not_between').then((channel_id) => {
        const tag = Cypress._.random(100000, 999999)

        cy.login_from_user_index(conf, 0)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.organize_freestyle_game(tag, 'question', 'truth')

        cy.login_from_user_index(conf, 1)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.guess_click(tag)
        cy.guess_type('g1')
        cy.wait(25000)
        cy.guess_submit()

        cy.contains(`${tag}: Your guess: g1`)
        cy.contains('It will not be taken into account because the guessing deadline has passed!')
      })
    })
  })
})