var wallPage = angular.module('wallPage')

wallPage.factory('postFactory',function($http){
	var factory = {}

	factory.getCurrentUser = function(callback){
		$http.get('http://localhost:5000/currentUser').success(function(output) {
			user = output;
			console.log("user is" , user);
			callback(user);
		});

	}
	factory.submitPost = function(post_message_info){
		$http.post('http://localhost:5000/userPost', {"post_message": post_message_info}).success(function(output){

		});
	}
	return factory
});