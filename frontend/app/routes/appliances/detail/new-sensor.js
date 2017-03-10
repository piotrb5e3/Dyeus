import Ember from 'ember';

export default Ember.Route.extend({
  model() {
    const appliance = this.modelFor('appliances.detail');
    return this.get('store').createRecord('sensor', {appliance: appliance});
  }
});
