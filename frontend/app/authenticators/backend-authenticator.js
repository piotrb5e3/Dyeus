import Ember from 'ember';
import Base from 'ember-simple-auth/authenticators/base';
import ENV from 'frontend/config/environment';

const NAMESPACE_PART = ENV.APP.API_NAMESPACE ? `/${ENV.APP.API_NAMESPACE}` : "";
const API_BASE = `${ENV.APP.API_HOST}${NAMESPACE_PART}`;

export default Base.extend({
  ajax: Ember.inject.service(),

  authenticatePath: `${API_BASE}/auth/gettoken`,
  testPath: `${API_BASE}/auth/test`,
  getUserDataPath: `${API_BASE}/user`,

  restore(data) {
    return this.get('ajax').request(this.get("testPath"), {
      method: 'GET',
      headers: {
        'Authorization': `Token ${data.token}`,
      },
      data: {},
    }).then(() => data);
  },

  authenticate(login, password) {
    return this.get('ajax').request(this.get("authenticatePath"), {
      method: 'POST',
      data: {
        username: login,
        password: password,
      },
    }).then((authResponse) => {
      console.log(authResponse);
      return this.get('ajax').request(this.get("getUserDataPath"), {
        method: 'GET',
        headers: {
          'Authorization': `Token ${authResponse.token}`,
        },
      }).then((userDataResponse) => {
        return {
          token: authResponse.token,
          username: userDataResponse.username,
        };
      });
    });
  }
});
