var login_register = angular.module('login_register')
login_register.controller('usersController',function($scope,$location,$window,userFactory){
	$scope.show_form = true
	$scope.registerUser = function() {
		userFactory.registerUser($scope.new_user,function(data){
			$scope.current_user = data.username
			$scope.user_id = data.user_id
			$scope.show_form = false
			//To build a SPA , use $location to trigger a view after an action has been performed
			$location.path('/home')
			//Use window module to redirect to another page -a tottaly different location like www.google.com (not a SPA) 
			//$window.location = '/views/wall_page.html'  
		});
	}
	$scope.loginUser = function(){
		userFactory.loginUser($scope.user,function(data){
			$scope.current_user = data.username
			$scope.user_id = data.user_id
			$scope.show_form = false
			$location.path('/home')
			//$window.location = '/partials/wall_page.html'
		});
	}
});