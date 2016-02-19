//var wallPage = angular.module('wallPage')
var login_register = angular.module('login_register')

login_register.factory('postFactory',function($http){
	var factory = {}

	factory.get_all_posts_comments = function(callback){
		$http.get('http://localhost:5000/users/posts/comments').success(function(output){
			console.log("Allposts with comments are", output.result)
			callback(output.result)
		});
	}
	factory.getCurrentUser = function(callback){
		$http.get('http://localhost:5000/users').success(function(output) {
			user = output;
			console.log("user is" , user);
			callback(user);
		});

	}
	factory.submitPost = function(post_message_info,callback){
		console.log("form data is ",post_message_info)
		$http.post('http://localhost:5000/users/posts', post_message_info).success(function(output){
			console.log("Post id is", output)
			callback(output)
		});
	}
	factory.submitComment = function(comment_info,post_id,callback){
		console.log("comment data is",comment_info)
		$http.post('http://localhost:5000/users/posts/' + post_id + '/comments', comment_info).success(function(output){
			console.log("Comment id is", output)
			callback(output)
		});
	}
	factory.updateComment = function(edit_comment,post_id,comment_id,callback){
		console.log("data,postid,commentid",edit_comment,post_id,comment_id)
		$http.put('http://localhost:5000/users/posts/'+ post_id + '/comments/' + comment_id ,edit_comment).success(function (output) {
			console.log("UPdate output is",output)
			callback(output)
		});
	}
	return factory
});