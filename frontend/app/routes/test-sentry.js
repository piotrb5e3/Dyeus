import Ember from 'ember';

export default Ember.Route.extend({
  beforeModel(){
    this.get('raven').captureException(new Error("Test error"));
    this.transitionTo('application');
  }
});
