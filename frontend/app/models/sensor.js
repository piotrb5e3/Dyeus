import DS from 'ember-data';
import {instanceOp} from 'ember-api-actions';

export default DS.Model.extend({
  name: DS.attr('string'),
  code: DS.attr('string'),
  appliance: DS.belongsTo('appliance'),
  recent: instanceOp(
    {
      path: 'recent/',
      type: 'GET',

    }),
});
