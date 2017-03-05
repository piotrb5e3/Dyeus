import Ember from 'ember';

export default Ember.Controller.extend({
  session: Ember.inject.service('session'),
  actions: {
    goToRoute(route){
      this.transitionToRoute(route);
    },
    logout(){
      this.get('session').invalidate();
    }
  }
});
