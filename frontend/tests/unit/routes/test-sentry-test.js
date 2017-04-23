import { moduleFor, test } from 'ember-qunit';

moduleFor('route:test-sentry', 'Unit | Route | test sentry', {
  needs: ['service:metrics']
});

test('it exists', function(assert) {
  let route = this.subject();
  assert.ok(route);
});
