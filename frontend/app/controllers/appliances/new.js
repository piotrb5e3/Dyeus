import Ember from 'ember';

export default Ember.Controller.extend({
  actions: {
    submitNewAppliance() {
      this.get('model').save()
        .then(() => this.transitionToRoute('appliances'))
        .catch((err) => console.log(err));
    },
    setAuthModel(value /*, event */) {
      this.get('model').set('authenticationModel', value);
    }
  }
});
