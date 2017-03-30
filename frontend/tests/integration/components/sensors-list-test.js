import {moduleForComponent, test} from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('sensors-list', 'Integration | Component | sensors list', {
  integration: true
});

test('it renders', function (assert) {
  this.set('model', {
    id: 0,
    sensors: [
      {
        id: 0,
        name: "S0",
        code: "s0",
        appliance: 0,
      },
      {
        id: 1,
        name: "S1",
        code: "s1",
        appliance: 0,
      },
    ]
  });

  this.on('goToSensor', function () {
  });
  this.on('goToAddSensor', function () {
  });

  this.render(hbs`{{sensors-list appliance=model goToSensor=(action 'goToSensor') addSensor=(action 'goToAddSensor')}}`);

  assert.ok(this.$().text().trim().includes("S0"));
  assert.ok(this.$().text().trim().includes("S1"));
});
