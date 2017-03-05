import Ember from 'ember';

export default Ember.Controller.extend({
  authenticationModel: null,
  authModelSelectValues: ["token"],
  authModelsVerbose: {
    "token": "Token over HTTPS",
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
