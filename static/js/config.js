/**
 * INSPINIA - Responsive Admin Theme
 *
 * Inspinia theme use AngularUI Router to manage routing and views
 * Each view are defined as state.
 * Initial there are written state for all view in theme.
 *
 */
function config($stateProvider, $urlRouterProvider, $ocLazyLoadProvider, jwtInterceptorProvider, $httpProvider, FacebookProvider) {
    jwtInterceptorProvider.tokenGetter = function() {
      return localStorage.get('jwt');
    }

    //$httpProvider.interceptors.push('jwtInterceptor');
    FacebookProvider.init('1295136350574737');
    $urlRouterProvider.otherwise("/index/dashboard");
    console.log("at static_url", static_url);
    var static_url = "/static/";
    $ocLazyLoadProvider.config({
        // Set to true if you want to see what and when is dynamically loaded
        debug: false
    });

    $stateProvider

        .state('index', {
            abstract: true,
            url: "/index",
            authenticate: false,
            templateUrl: static_url + "views/common/content.html",
        })
        .state('index.main', {
            url: "/main",
            authenticate: true,
            templateUrl: static_url + "views/main.html",
            data: { pageTitle: 'Example view' }
        })
        .state('index.minor', {
            url: "/minor",
            authenticate: false,
            templateUrl: static_url + "views/minor.html",
            data: { pageTitle: 'Example view' }
        })
        .state('login', {
            url: "/login",
            authenticate: false,
            controller: 'loginController',
            templateUrl: static_url + "views/login.html",
            data: { pageTitle: "login"}
        })
        .state('index.dashboard', {
            url: "/dashboard",
            authenticate: true,
            controller: 'registerController',
            templateUrl: static_url + "views/dashboard.html",
            data: { pageTitle: "dashboard"}  
        })

}
angular
    .module('inspinia')
    .config(config)
    .run(function($rootScope, $state, AuthService, $window) {
        console.log("user ******" , JSON.stringify($window.localStorage.currentUser));
        $rootScope.$state = $state;
        $rootScope.$on("$stateChangeSuccess", function(event, toState, toParams, fromState, fromParams){
            console.log("at stateChangeStart ", toState.authenticate, toState);
            if (toState.authenticate && !$window.localStorage.currentUser) {
                console.log("st login");
                $state.transitionTo("login");
                event.preventDefault(); 
            }
        });
    });

/*function run($rootScope, $http, $location, $localStorage) {
        // keep user logged in after page refresh
        if ($localStorage.currentUser) {
            $http.defaults.headers.common.Authorization = 'Bearer ' + $localStorage.currentUser.token;
        }
 
        // redirect to login page if not logged in and trying to access a restricted page
        $rootScope.$on('$locationChangeStart', function (event, next, current) {
            var publicPages = ['/login'];
            var restrictedPage = publicPages.indexOf($location.path()) === -1;
            if (restrictedPage && !$localStorage.currentUser) {
                $location.path('/login');
            }
        });
}
        $rootScope.$on("$stateChangeStart", function(event, toState, toParams, fromState, fromParams){
            AuthService.getUserStatus()
                .then(function(){
                    //console.log("at run &&&&&&7", next.access.restricted, AuthService.isLoggedIn(), next, current)
                    if (toState.authenticate && !AuthService.isLoggedIn()){
                        //$location.path('/register');
                        //$location.path('/login');
                        //$route.reload();
                        $state.transitionTo("login");
                        event.preventDefault(); 
                    } else {
                        //$location.path('/dashboard');
                        console.log("at login service ******* success")
                    }
                });
        });*/