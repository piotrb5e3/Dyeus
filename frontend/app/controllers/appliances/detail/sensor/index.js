import Ember from 'ember';

export default Ember.Controller.extend({
  chartOptions: {
    chart: {
      zoomType: 'x'
    },
    xAxis: {
      type: 'datetime'
    },
    yAxis: {
      title: {
        text: 'Value'
      }
    },
    legend: {
      enabled: false
    },
  },
  recent: {values: []},
  recentObserver: Ember.observer('model', function () {
    return this.get('model').recent().then((data) => this.set('recent', data));
  }),
  chartData: Ember.computed('recent', function () {
    const values = this.get('recent').values.map(([x, y]) => [Date.parse(x), parseFloat(y)]);
    console.log(values);
    return [{
      type: 'line',
      name: 'Plot',
      data: values,
    }];
  }),
  actions: {
    deleteSensor() {
      const model = this.get('model');
      const appliance = model.get('appliance');
      this.get('model').destroyRecord()
        .then(() => this.transitionToRoute('appliances.detail', appliance));
    }
  }
});
