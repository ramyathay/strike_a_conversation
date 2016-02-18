var login_register = angular.module('login_register')
login_register.controller('usersController',function($scope,userFactory){
	$scope.getCurrentUser = function(){
		$scope.current_user = userFactory.getCurrentUser()
		console.log($scope.current_user)
	}
	$scope.registerUser = function() {
		userFactory.registerUser($scope.new_user)
	}
	$scope.loginUser = function(){
		userFactory.loginUser($scope.user)
	}
	$scope.getCurrentUser()
});