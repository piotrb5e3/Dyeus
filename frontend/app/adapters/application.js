import DataAdapterMixin from 'ember-simple-auth/mixins/data-adapter-mixin';
import DRFAdapter from './drf';

export default DRFAdapter.extend(DataAdapterMixin, {
  authorizer: 'authorizer:backend-authorizer'
});
