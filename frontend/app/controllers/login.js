import Ember from 'ember';

export default Ember.Controller.extend({
  session: Ember.inject.service('session'),
  login: "",
  password: "",
  actions: {
    authenticate() {
      let {login, password} = this.getProperties('login', 'password');
      this.get('session').authenticate('authenticator:backend-authenticator', login, password)
        .then(()=> {
          this.transitionToRoute('index')
        })
        .catch((err) => {
          console.log(err);
          this.set('errorMessage', 'Authentication failed');
        });
    }
  }
});
