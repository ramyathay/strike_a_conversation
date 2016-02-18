var login_register = angular.module('login_register',['ngMessages','ngRoute'])
//Use routeProvider here if any partials have to be included
login_register.config(function ($routeProvider,$locationProvider){
	$routeProvider
	.when('/home', {
		templateUrl: '/partials/wall_page.html'
	})	
	.otherwise({
		redirectTo: '/'
	});
	$locationProvider.html5Mode(true);
});
		