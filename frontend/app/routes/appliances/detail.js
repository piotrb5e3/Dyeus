import Ember from 'ember';

export default Ember.Route.extend({
  model(params) {
    return this.get('store').find('appliance', params.appliance_id);
  },
  actions: {
    reloadAppliance() {
      this.refresh();
    }
  }
});
