import {moduleForComponent, test} from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('sensors-list-item', 'Integration | Component | sensors list item', {
  integration: true
});

test('it renders', function (assert) {
  this.set('sensor', {
    id: 0,
    name: "S0",
    code: "s0",
    appliance: 0,
  });

  this.on('goToSensor', function () {
  });

  this.render(hbs`{{sensors-list-item sensor=sensor goToSensor=(action 'goToSensor')}}`);

  assert.ok(this.$().text().trim().includes("S0"));
  assert.notOk(this.$().text().trim().includes("S1"));

});
