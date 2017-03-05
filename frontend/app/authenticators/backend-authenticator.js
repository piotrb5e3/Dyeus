import Ember from 'ember';
import Base from 'ember-simple-auth/authenticators/base';

export default Base.extend({
  ajax: Ember.inject.service(),

  authenticatePath: 'http://localhost:8000/auth/gettoken',
  testPath: 'http://localhost:8000/auth/test',
  getUserDataPath: 'http://localhost:8000/user',

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
