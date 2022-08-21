describe('main', () => {

  it('main', () => {

    cy.get_conf().then((conf) => {
      cy.get_channel_id('exception_slash_command_max_running').then((channel_id) => {
        const tag1 = Cypress._.random(100000, 999999)
        const tag2 = Cypress._.random(100000, 999999)
        const tag3 = Cypress._.random(100000, 999999)
        cy.login_from_user_index(conf, 0)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.organize_freestyle_game(tag1, 'question', 'truth')
        cy.organize_freestyle_game(tag2, 'question', 'truth')
        cy.organize_freestyle_game(tag3, 'question', 'truth')
        cy.slash_freestyle('tag')
        cy.contains('There are already 3 games running! This is the maximal number allowed.')
        cy.mark_game_as_success(tag1)
        cy.mark_game_as_success(tag2)
        cy.mark_game_as_success(tag3)
      })
    })
  })
})
