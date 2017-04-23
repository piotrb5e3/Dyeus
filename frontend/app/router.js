import Ember from 'ember';
import config from './config/environment';

const Router = Ember.Router.extend({
  location: config.locationType,
  rootURL: config.rootURL,

  metrics: Ember.inject.service(),

  didTransition() {
    this._super(...arguments);
    this._trackPage();
  },

  _trackPage() {
    Ember.run.scheduleOnce('afterRender', this, () => {
      const page = this.get('url');
      const title = this.getWithDefault('currentRouteName', 'unknown');

      Ember.get(this, 'metrics').trackPage({page, title});
    });
  }
});

Router.map(function () {
  this.route('login');
  this.route('appliances', function () {
    this.route('detail', {path: ":appliance_id"}, function () {
      this.route('sensor', {path: "sensor/:sensor_id"}, function () {
      });
      this.route('new-sensor');
      this.route('manage-auth');
    });
    this.route('new');
  });
  this.route('logout');
  this.route('about');
  this.route('test-sentry');
});

export default Router;
