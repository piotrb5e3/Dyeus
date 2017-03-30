import { moduleForModel, test } from 'ember-qunit';

moduleForModel('appliance', 'Unit | Model | appliance', {
  // Specify the other units that are required for this test.
  needs: ['model:sensor']
});

test('it exists', function(assert) {
  let model = this.subject();
  assert.ok(!!model);
});
