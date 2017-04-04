import DS from 'ember-data';
import {instanceOp} from 'ember-api-actions';

export default DS.Model.extend({
  name: DS.attr('string'),
  isActive: DS.attr('boolean'),
  authenticationModel: DS.attr('string'),
  authenticationValue: DS.attr('string'),
  sensors: DS.hasMany('sensor'),
  activate: instanceOp(
    {
      path: 'activate/',
      type: 'POST',
    }),
  deactivate: instanceOp(
    {
      path: 'deactivate/',
      type: 'POST',
    }),
});
