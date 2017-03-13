import Ember from 'ember';

export default Ember.Route.extend({
  session: Ember.inject.service('session'),
  beforeModel(/* transition */) {
    if (!this.get('session').get('isAuthenticated')) {
      this.transitionTo('about');
    }
  }
});
