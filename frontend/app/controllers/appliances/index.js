import Ember from 'ember';

export default Ember.Controller.extend({
  panelActions: Ember.inject.service(),
  actions: {
    goToAppliance(appliance){
      this.transitionToRoute('appliances.detail', appliance);
    },
    goToAddAppliance(){
      this.transitionToRoute('appliances.new');
    },
  }
});
