import { moduleFor, test } from 'ember-qunit';

moduleFor('route:appliances/detail/index', 'Unit | Route | appliances/detail/index', {
  needs: ['service:metrics']
});

test('it exists', function(assert) {
  let route = this.subject();
  assert.ok(route);
});
