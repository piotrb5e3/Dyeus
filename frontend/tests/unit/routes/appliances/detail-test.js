import { moduleFor, test } from 'ember-qunit';

moduleFor('route:appliances/detail', 'Unit | Route | appliances/detail', {
  needs: ['service:metrics']
});

test('it exists', function(assert) {
  let route = this.subject();
  assert.ok(route);
});
