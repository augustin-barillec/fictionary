describe('main', () => {
  it('main', () => {
    cy.get_conf().then((conf) => {
      cy.get_channel_id('english_exception_slash_command_invalid_parameter').then((channel_id) => {
        cy.login_from_user_index(conf, 0)
        cy.go_to_channel_from_channel_id(conf, channel_id)
        cy.slash_command('tag', 'toto')
        cy.contains("Le paramètre de la commande doit être l'un des suivants : freestyle, automatic ou help.")
      })
    })
  })
})
