var wallPage = angular.module('wallPage');
wallPage.controller('postsController',function($scope,postFactory){
	$scope.submitPost = function(){
		postFactory.submitPost($scope.newPost,function(data){
			console.log("REceived post id ",data)
		});
		$scope.get_all_posts_comments();
	}
	$scope.get_all_posts_comments = function(data){
		console.log("Entered get_all_posts_comments")
		postFactory.get_all_posts_comments(function(data){
			$scope.posts_comments = data
			$scope.current_user = 'Ramyatha yugendernath'
		});
	}
	$scope.submitComment = function(comment_form, post_id) {
		console.log("Comment form data ",comment_form, post_id)
		postFactory.submitComment(comment_form,post_id,function(data){
			console.log("REceived comment id ",data)
		});
		$scope.get_all_posts_comments();
	}
	$scope.get_all_posts_comments();
});