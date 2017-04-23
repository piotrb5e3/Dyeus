import { moduleFor, test } from 'ember-qunit';

moduleFor('route:appliances/detail/new-sensor', 'Unit | Route | appliances/detail/new sensor', {
  needs: ['service:metrics']
});

test('it exists', function(assert) {
  let route = this.subject();
  assert.ok(route);
});
