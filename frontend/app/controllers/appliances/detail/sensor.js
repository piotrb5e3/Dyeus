import Ember from 'ember';

export default Ember.Controller.extend({
  actions: {
    goToAppliance(sensor){
      this.transitionToRoute("appliances.detail", sensor.get('appliance'));
    }
  }
});
