import { moduleFor, test } from 'ember-qunit';

moduleFor('route:appliances/detail/manage-auth', 'Unit | Route | appliances/detail/manage auth', {
  needs: ['service:metrics']
});

test('it exists', function(assert) {
  let route = this.subject();
  assert.ok(route);
});
