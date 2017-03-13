import Ember from 'ember';

export default Ember.Controller.extend({
  authenticationModel: null,
  authModelSelectValues: ["token", "gcm_aes"],
  authModelsVerbose: {
    "token": "Token over HTTPS",
    "gcm_aes": "AES128 in GCM mode (no HTTPS required)"
  },
  actions: {
    submitNewAppliance() {
      const model = this.get('model');
      model.save()
        .then(() => this.transitionToRoute('appliances'))
        .catch((err) => console.log(err));
    }
  }
});
