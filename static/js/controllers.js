/**
 * INSPINIA - Responsive Admin Theme
 *
 */

/**
 * MainCtrl - controller
 */
function MainCtrl($window) {

    this.userName = $window.localStorage.currentUser;
    this.helloText = 'Welcome in SeedProject';
    this.descriptionText = 'It is an application skeleton for a typical AngularJS web app. You can use it to quickly bootstrap your angular webapp projects and dev environment for these projects.';

};


function loginController ($scope, $state, Facebook, FacebookService, $window) {

  $scope.getLoginStatus = function() {
      Facebook.getLoginStatus(function(response) {
        console.log("response at Facebook status", response);
        if(response.status === 'connected') {
          $scope.loggedIn = true;
          //$scope.removeAuth();
          //$scope.fbLogout();
          var authResponse = response.authResponse;          
          //FacebookService.sendToken(authResponse.accessToken);
        } else {
          $scope.loggedIn = false;
        }
      });
  };
  //$scope.getLoginStatus();
  
  $scope.fbLogout = function () {
    Facebook.logout(function(response){

      console.log("at fbLogout *******", response);
    });
  };

  $scope.login = function() {
      // From now on you can use the Facebook service just as Facebook api says
      Facebook.login(function(response) {
        if(response.status === 'connected') {
          $scope.loggedIn = true;
          var authResponse = response.authResponse;          
          FacebookService.sendToken(authResponse.accessToken, authResponse.userID)
            .then(function (data) {
              $window.localStorage.setItem("currentUser", data.name);
              $window.localStorage.setItem("token", data.auth_token);
              $state.transitionTo("index.dashboard");
            });

        }
        console.log("at login **********", response); 
        // Do something with response.
      }, {scope: 'manage_pages,email'});
  };
};

function registerController ($scope, $state, PageService, $uibModal) {	
  $scope.pages  = [{"category":"Local Business","page_id":"1752744235019776","name":"Cafe"}];
  $scope.getUsers = function () {
    PageService.fetchPages()
      .then(function (data) {
        var pages = PageService.getPages();
        $scope.pages.length = 0;
        $scope.pages = pages;
        console.log("pages ********", $scope.pages, typeof($scope.pages));
      });
  };
  $scope.getUsers();
  $scope.update = function (page_id) {
          console.log("page_id", page_id);
          PageService.getId(page_id);
          var modalInstance = $uibModal.open({
              templateUrl: 'static/views/modal_example2.html',
              controller: 'updateController',
              windowClass: "animated flipInY"
          });
  };
};

function updateController($scope, $state, PageService, $uibModalInstance) {
  console.log("update controller", PageService.getId());
  $scope.price = {
       val: ''
  };
  $scope.parking = {
     lot: false,
     valet: false,
     street: false
  };
  $scope.hours = {
    value1: false,
    value2: false,
    value3: false,
    value4: false,
    value5: false,
    value6: false,
    value7: false
  };
  var avialable_days = [
    "mon_1_open",
    "tue_1_open",
    "wed_1_open",
    "thu_1_open",
    "fri_1_open",
    "sat_1_open",
    "sun_1_open",
  ];

  function setInfo(){
    PageService.getPageInfo()
      .then(function (data){
        console.log("data", data);
        var page_data = data.pages;
        if ("price_range" in page_data) {
          var price_range = page_data.price_range,
             length = price_range.length,
             out = "";
          out = Array(length+1).join("$");
          $scope.price.val = out;
        } 
        if ("parking" in page_data){
          var parking = page_data.parking;
          angular.forEach(parking, function(value, key) {
            var val = value ? true : false;
            $scope.parking[key] = val;
          });

        }
        if ("hours" in page_data){
          var hours = page_data.hours;
          angular.forEach(hours, function(value, key) {
            var index = avialable_days.indexOf(key);
            if (index!==-1){
              val = "value"+(index+1);
              $scope.hours[val] = true
            }
          });
        }
        
      });

  };
  setInfo();
  $scope.ok = function () {
    
    $uibModalInstance.close();
    var parking = $scope.parking, 
      price_range = $scope.price, 
      hours = $scope.hours,
      h = {},
      update_data = {};

    if (price_range.val) {
      price_range = price_range.val
      update_data["price_range"] = price_range; 
    }
    if (parking) {
      flag = false;
      angular.forEach(parking, function(value, key) {
        var val = value ? 1 : 0;
        parking[key] = val;
      });
      update_data["parking"] = parking;    
    }
    if (hours) {
      var i=0;
      angular.forEach(hours, function(value, key) {  
        var key_r = "";

        if (value) {
          key_r = avialable_days[i];
          key_list = key_r.split("_");
          key_list[2] = "close";
          key_c = key_list.join("_")
          h[key_r] = "09:00";
          h[key_c] = "17:00";
        }
        i = i + 1;
      });
      update_data["hours"] = h      
    }
    console.log("update_data *******", update_data);
    PageService.updatePage(update_data);
  };

  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };
};

function logoutController($scope, $state, $window) {
  $scope.logout = function() {
    $window.localStorage.clear();
    $state.transitionTo("login");
  };
};

angular
    .module('inspinia')
    .controller('MainCtrl', ['$window', MainCtrl])
    .controller('loginController', ['$scope', '$state', 'Facebook', 'FacebookService', '$window', loginController])
    .controller('registerController', ['$scope', '$state', 'PageService', '$uibModal', registerController])
    .controller('logoutController', ['$scope', '$state', '$window', logoutController])
    .controller('updateController', ['$scope', '$state', 'PageService', '$uibModalInstance', updateController]);
