var my_app = angular.module('inspinia');
my_app.factory('AuthService',
  ['$q', '$timeout', '$http', '$window',
  function ($q, $timeout, $http, $window) {
    return {
      login: login,
      register: register,
      getAllusers: getAllusers
    };
/*  function login(email, password) {

    // create a new instance of deferred
    var deferred = $q.defer();

    // send a post request to the server
    $http.post('/api/login', {email: email, password: password})
      // handle success
      .success(function (data, status) {
        if(status === 200 && data.data.email){
          user = true;
          user_role = data.data.roles;
          user_data = data.data;
          deferred.resolve();
        } else {
          user = false;
          deferred.reject();
        }
      })
      // handle error
      .error(function (data) {
        user = false;
        deferred.reject();
      });

    // return promise object
    return deferred.promise;

  };*/
  function login(email, password) {
    var deferred = $q.defer();

    $http.post('/account/login/', {email: email, password: password})
      // handle success
      .success(function (data, status) {
        var username = data.username || "unknown";
        
        if (data.token) {

          $window.localStorage.currentUser = { username: username, token: data.token };
          // add jwt token to auth header for all requests made by the $http service
          $http.defaults.headers.common.Authorization = 'Bearer ' + data.token;
          deferred.resolve();
        } else {
          deferred.reject();
        }
      })
      .error(function (data) {
        deferred.reject();
      });
    return deferred.promise;
  }

  function register(data) {
    var deferred = $q.defer();

    $http.post('/account/register/', data)
      // handle success
      .success(function (data, status) {
        console.log("data at register", data, status);
        var username = data.username || "unknown";
        console.login
        if (data) {
          //$window.localStorage.currentUser = { username: username, token: data.token };
          // add jwt token to auth header for all requests made by the $http service
          //$http.defaults.headers.common.Authorization = 'Bearer ' + data.token;
          deferred.resolve();
        } else {
          deferred.reject();
        }
      })
      .error(function (data) {
        deferred.reject();
      });
    return deferred.promise;
  }

  function getAllusers() {
    var deferred = $q.defer();

    $http.get('/account/register/')
      .success(function (data) {
        if (data) {
          deferred.resolve(data)
        } else {
          deferred.reject();
        }
      })
      .error(function (data) {
        deferred.reject();
      });
    return deferred.promise;

    };
  
}]);

my_app.factory('FacebookService',
  ['$q', '$timeout', '$http',
  function ($q, $timeout, $http) {
  return {
    sendToken: sendToken
  };

  function sendToken(token, fb_id) {
      var deferred = $q.defer(),
        token = token;
   
      $http.post('/account/send_auth_token/', {token: token, fb_id: fb_id})
        .success(function (data, status) {
          console.log("data", data, status);
          if(status === 201) {
            //return data.data.keyword
            deferred.resolve(data);
              //return data.data.keyword
          } else {
            deferred.reject();
          }
        })
        .error(function (data) {
          deferred.reject();
          console.log("not succs sendToken")
        });

      return deferred.promise;
  };
}]);

my_app.factory('PageService',
  ['$q', '$timeout', '$http', '$window',
  function ($q, $timeout, $http, $window) {
  return {
    sendToken: sendToken
  };

  function sendToken(token, fb_id) {
      var deferred = $q.defer(),
        token = token;
   
      $http.post('/account/send_auth_token/', {token: token, fb_id: fb_id})
        .success(function (data, status) {
          console.log("data", data, status);
          if(status === 201) {
            //return data.data.keyword
            deferred.resolve(data);
              //return data.data.keyword
          } else {
            deferred.reject();
          }
        })
        .error(function (data) {
          deferred.reject();
          console.log("not succs sendToken")
        });

      return deferred.promise;
  };
  function getPages() {
    Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
    var deferred = $q.defer(),
      headers = {headers:  {
        'Authorization': 'Token '+ $window.localStorage.getItem("token");
      };

    $http.get('/account/pages/')
      .success(function (data) {
        if (data) {
          deferred.resolve(data)
        } else {
          deferred.reject();
        }
      })
      .error(function (data) {
        deferred.reject();
      });
    return deferred.promise;
  };
}]);