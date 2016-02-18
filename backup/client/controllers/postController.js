//var wallPage = angular.module('wallPage');
wallPage.controller('postsController',function($scope,postFactory){
	$scope.getCurrentUser = function(){
		 postFactory.getCurrentUser(function(data){
			$scope.current_user = data
		});
	}
	$scope.submitPost = function(){
		postFactory.submitPost($scope.user_post)
	}
	$scope.getCurrentUser();
});