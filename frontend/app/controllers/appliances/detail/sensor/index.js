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
  chartData: Ember.computed('model', function () {
    const values = this.get('model').values.map(([x, y]) => [Date.parse(x), parseFloat(y)]);
    console.log(values);
    return [{
      type: 'line',
      name: 'Plot',
      data: values,
    }];
  }),
});
