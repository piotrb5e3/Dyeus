import Ember from 'ember';

export default Ember.Controller.extend({
  session: Ember.inject.service('session'),
  login: "",
  password: "",
  actions: {
    authenticate() {
      let {login, password} = this.getProperties('login', 'password');
      console.log({login, password});
      this.get('session').authenticate('authenticator:backend-authenticator', login, password)
        .then(() => this.transitionToRoute('index'))
        .then(() => {
          this.set('login', '');
          this.set('password', '');
        })
        .catch((err) => {
          console.log(err);
          this.set('errorMessage', 'Authentication failed');
        });
    }
  }
});
