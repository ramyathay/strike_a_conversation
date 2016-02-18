var login_register = angular.module('login_register')
login_register.factory('userFactory',function($http){
	var factory = {};
	factory.registerUser = function(newUser,callback){
		$http.post('http://localhost:5000/register',newUser).success(function(output){
			console.log("Factory received data",output)
			callback(output)
		});
	}
	factory.loginUser = function(user,callback){
		$http.post('http://localhost:5000/login',user).success(function(output){
			console.log("Factory received data",output)
			callback(output)
		});
	}
	return factory;
});