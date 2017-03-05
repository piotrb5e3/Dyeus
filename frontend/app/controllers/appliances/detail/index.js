import Ember from 'ember';

export default Ember.Controller.extend({
  actions: {
    goToSensor(sensor) {
      this.transitionToRoute('appliances.detail.sensor', sensor.get('appliance'), sensor);
    }
  }
});
