describe('main', () => {
  it('main', () => {
    cy.get_conf().then((conf) => {
      cy.get_channel_id('english_exception_slash_command_not_invited').then((channel_id) => {
        cy.login_from_user_index(conf, 0)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.slash_freestyle('tag')
        cy.contains("L'application Fictionary n'est pas dans la conversation.")
      })
    })
  })
})
