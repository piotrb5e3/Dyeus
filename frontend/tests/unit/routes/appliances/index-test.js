import { moduleFor, test } from 'ember-qunit';

moduleFor('route:appliances/index', 'Unit | Route | appliances/index', {
  needs: ['service:metrics']
});

test('it exists', function(assert) {
  let route = this.subject();
  assert.ok(route);
});
