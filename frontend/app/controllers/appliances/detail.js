import Ember from 'ember';

export default Ember.Controller.extend({
  actions: {
    goToAppliances(){
      this.transitionToRoute("appliances");
    }
  }
});
