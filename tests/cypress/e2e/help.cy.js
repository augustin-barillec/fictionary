describe('main', () => {
  it('main', () => {
    cy.get_conf().then((conf) => {
      cy.get_channel_id('help').then((channel_id) => {
        cy.login_from_user_index(conf, 0)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.slash_command('help', 'tag')
        cy.contains('This is a slack app to play fictionary. All infos are available here.')
      })
    })
  })
})
