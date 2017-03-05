import Ember from 'ember';
import DataRoute from 'ember-data-route';

export default Ember.Route.extend(DataRoute, {
  model() {
    return this.get('store').createRecord('appliance');
  }
});
