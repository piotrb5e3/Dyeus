import { moduleFor, test } from 'ember-qunit';

moduleFor('route:appliances/detail/sensor', 'Unit | Route | appliances/detail/sensor', {
  needs: ['service:metrics']
});

test('it exists', function(assert) {
  let route = this.subject();
  assert.ok(route);
});
