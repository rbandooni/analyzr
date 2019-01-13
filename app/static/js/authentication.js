

// provider.setCustomParameters({
// 	'login_hint': 'username@email.com'
// });

function loginWithEmail() {
	var email = document.getElementsByName('email')[0].value;
	var password = document.getElementsByName('password')[0].value;
	firebase.auth().createUserWithEmailAndPassword(email, password).catch(function(error) {
  // Handle Errors here.
  var errorCode = error.code;
  var errorMessage = error.message;
  if(error.code == 'auth/user-not-found') {
  	swal({
  		title: 'Email not found',
  		text: error.message,
  		icon: 'warning',
  		dangerMode: false,
  		button: {
  			text: 'Try Again'
  		}
  	})
  }
  else if(error.code == 'auth/wrong-password') {
  	swal({
  		title: 'Login Error',
  		text: error.message,
  		icon: 'error',
  		dangerMode: true,
  		button: {
  			text: 'Try Again'
  		}
  	})
  }
  else {
  	console.log('errorCode',error.code);
  }
});
	// firebase.auth().signInWithEmailAndPassword(email, password).catch( function(error) {

	// })
}

function loginWithFacebookPopup() {
	var provider = new firebase.auth.FacebookAuthProvider();
	provider.addScope('user_birthday');
	firebase.auth().useDeviceLanguage();
	provider.setCustomParameters({
		'display': 'popup'
	})
	firebase.auth().signInWithPopup(provider).then( function(result) {
		var token = result.credentials.accessToken;
		var user = result.user;
		window.location.href = "/";
	}).catch( function(error) {
		console.log(error.code);
	})
}

function loginWithGooglePopup() {
	var provider = new firebase.auth.GoogleAuthProvider();
	firebase.auth().signInWithPopup(provider).then(function (result) {
		var token = resule.credentials.accessToken;
		var user = result.user;
		var displayName = user.displayName;
		var email = user.email;
		var emailVerified = user.emailVerified;
		var photoURL = user.photoURL;
		var uid = user.uid;
		var phoneNumber = user.phoneNumber;
		var providerData = user.providerData;
		swal('Logging you in...', {
			buttons: false
		})
		window.location.href = "/";
	}).catch( function(error) {
		var errorCode = error.code;
		var errorMessage = error.message;
		var email = error.mail
		var credential = error.credential;


	});
}

function signOut() {
	swal({
		title: 'Are you sure?',
		icon: 'warning',
		dangerMode: true,
		buttons: true,

	}).then(willLogout => {
		if(willLogout) {
			firebase.auth().signOut().then(function() {
				window.location.href = "/login";

			}).catch(function(error) {
				console.log(error);
			});
		}
	});

}