describe('main', () => {

  it('main', () => {

    cy.get_conf().then((conf) => {
      cy.get_channel_id('exception_slash_command_max_this_running').then((channel_id) => {
        cy.login_from_user_index(conf, 2)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.organize_freestyle_game('tag', 'question', 'truth')
        cy.organize_freestyle_game('tag', 'question', 'truth')
        cy.slash_freestyle('tag')
        cy.contains('You are already the organizer of 2 running games. This is the maximum number allowed.')
      })
    })
  })
})