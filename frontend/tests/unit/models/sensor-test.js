import {moduleForModel, test} from 'ember-qunit';

moduleForModel('sensor', 'Unit | Model | sensor', {
  // Specify the other units that are required for this test.
  needs: ['model:appliance']
});

test('it exists', function (assert) {
  let model = this.subject();
  assert.ok(!!model);
});
