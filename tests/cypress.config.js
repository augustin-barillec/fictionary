const { defineConfig } = require("cypress");

module.exports = defineConfig({
  chromeWebSecurity: false,
  watchForFileChanges: false,
  waitForAnimations: true,
  trashAssetsBeforeRuns: true,
  video: false,
  defaultCommandTimeout: 15000,

  e2e: {
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
  },
});
