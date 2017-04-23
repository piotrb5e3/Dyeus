import { moduleFor, test } from 'ember-qunit';

moduleFor('route:appliances', 'Unit | Route | appliances', {
  needs: ['service:metrics']
});

test('it exists', function(assert) {
  let route = this.subject();
  assert.ok(route);
});
