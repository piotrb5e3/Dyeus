import Ember from 'ember';

export default Ember.Controller.extend({
  authenticationModel: null,
  authModelSelectValues: ["token", "sha_hmac"],
  authModelsVerbose: {
    "token": "Token over HTTPS",
    "sha_hmac": "SHA256 MAC (no HTTPS required, no confidentiality)"
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
