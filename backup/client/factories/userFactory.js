var login_register = angular.module('login_register')
login_register.factory('userFactory',function($http){
	var factory = {};
	factory.getCurrentUser = function(callback){
		$http.get('/currentUser').success(function(output) {
			user = output;
			callback(user);
		});
	}
	factory.registerUser = function(newUser){
		$http.post('/registerUser',newUser).success(function(output){
			
		});
	}
	factory.loginUser = function(user){
		$http.post('/loginUser',user).success(function(output){

		});
	}
	return factory;
});