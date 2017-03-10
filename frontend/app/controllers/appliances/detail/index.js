import Ember from 'ember';

export default Ember.Controller.extend({
  actions: {
    goToSensor(sensor) {
      this.transitionToRoute('appliances.detail.sensor', sensor.get('appliance'), sensor);
    },
    activate() {
      this.get('model').activate()
        .then(() => this.send("reloadAppliance"));
    },
    deactivate() {
      this.get('model').deactivate()
        .then(() => this.send("reloadAppliance"));
    }
  }
});
