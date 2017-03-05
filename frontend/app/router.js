import Ember from 'ember';
import config from './config/environment';

const Router = Ember.Router.extend({
  location: config.locationType,
  rootURL: config.rootURL
});

Router.map(function () {
  this.route('login');
  this.route('appliances', function () {
    this.route('detail', {path: ":appliance_id"}, function () {
      this.route('sensor', {path: "sensor/:sensor_id"}, function() {
        this.route('recent');
      });
    });
    this.route('new');
  });
  this.route('logout');
});

export default Router;
