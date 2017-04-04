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
    },
    deleteAppliance() {
      this.get('model').destroyRecord()
        .then(() => this.transitionToRoute('appliances'));
    },
    goToAddSensor() {
      const model = this.get('model');
      this.transitionToRoute('appliances.detail.new-sensor', model);
    },
    goToManageAuth() {
      const model = this.get('model');
      this.transitionToRoute('appliances.detail.manage-auth', model);
    },
  }
});
