import { moduleFor, test } from 'ember-qunit';

moduleFor('route:appliances/detail/sensor/index', 'Unit | Route | appliances/detail/sensor/index', {
  needs: ['service:metrics']
});

test('it exists', function(assert) {
  let route = this.subject();
  assert.ok(route);
});
