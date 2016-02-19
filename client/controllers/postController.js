//var wallPage = angular.module('wallPage')
var login_register = angular.module('login_register')
console.log("Entered posts controller")

login_register.controller('postsController',function($scope,postFactory){
	console.log("Entered get_all_posts_comments")
	$scope.get_all_posts_comments = function(){
		postFactory.get_all_posts_comments(function(data){
			console.log("data received fro all post comments are",data)
			$scope.posts_comments = data
			// $scope.current_user = 'Ramyatha yugendernath'
			$scope.show_editComment = false
			$scope.show_editPost = false
			$scope.show_comment = true
		});
	}
	$scope.submitPost = function(){
		postFactory.submitPost($scope.newPost,function(data){
			console.log("REceived post id ",data)
		});
		$scope.get_all_posts_comments();
	}
	$scope.submitComment = function(comment_form, post_id) {
		console.log("Comment form data ",comment_form, post_id)
		postFactory.submitComment(comment_form,post_id,function(data){
			console.log("REceived comment id ",data)
		});
		$scope.get_all_posts_comments();
	}
	//Update and Delete
	$scope.updateComment = function(post_id,comment_id,comment_data) {
		console.log("comment Id",post_id,comment_id)
		postFactory.updateComment(comment_data,post_id,comment_id,function(data){
			console.log("REceived data",data);
		});
		$scope.show_editComment = true
		$scope.show_editPost = true
		$scope.show_comment = true
		$scope.get_all_posts_comments();
	}
	$scope.get_all_posts_comments();
});