describe('main', () => {

  it('main', () => {

    cy.get_conf().then((conf) => {
      cy.get_channel_id('exception_vote_submission_no_time_left').then((channel_id) => {
        const tag = Cypress._.random(100000, 999999)

        cy.login_from_user_index(conf, 0)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.organize_freestyle_game(tag, 'question', 'truth')

        cy.login_from_user_index(conf, 1)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.guess(tag, 'g1')

        cy.login_from_user_index(conf, 2)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.guess(tag, 'g2')

        cy.login_from_user_index(conf, 1)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.vote_click(tag)
        cy.vote_select('0')
        cy.wait(25000)
        cy.vote_submit()

        cy.contains(`${tag}: Your vote: proposal 2`)
        cy.contains('It will not be taken into account because the voting deadline has passed!')
      })
    })
  })
})