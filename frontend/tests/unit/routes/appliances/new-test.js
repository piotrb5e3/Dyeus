import { moduleFor, test } from 'ember-qunit';

moduleFor('route:appliances/new', 'Unit | Route | appliances/new', {
  needs: ['service:metrics']
});

test('it exists', function(assert) {
  let route = this.subject();
  assert.ok(route);
});
