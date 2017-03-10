import Ember from 'ember';

export default Ember.Controller.extend({
  actions: {
    submitNewSensor() {
      const model = this.get('model');
      model.save()
        .then(() => this.transitionToRoute('appliances.detail.sensor', model.get('appliance'), model))
        .catch((err) => console.log(err));
    }
  }
});
