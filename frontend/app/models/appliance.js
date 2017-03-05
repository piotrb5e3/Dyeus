import DS from 'ember-data';

export default DS.Model.extend({
  name: DS.attr('string'),
  isActive: DS.attr('boolean'),
  authenticationModel: DS.attr('string'),
  authenticationValue: DS.attr('string'),
  sensors: DS.hasMany('sensor'),
});
