window.addEventListener("load", function(){
  window.cookieconsent.initialise({
    "palette": {
      "popup": {
        "background": "#f5f5f5",
        "text": "#000000"
      },
      "button": {
        "background": "#237afc",
        "text": "#ffffff"
      }
    },
    "content": {
      "message": "We use cookies to enhance your user experience on our website. By clicking 'Accept', you consent to our use of cookies. To learn more, please read our <a href='/privacy-policy'>Privacy Policy</a>.",
      "dismiss": "Decline",
      "allow": "Accept",
      "link": "Learn more",
      "href": "/cookie-policy"
    },
    "cookie": {
      "name": "travel_website_cookie_consent",
      "expiryDays": 365,
      "path": "/"
    },
    onInitialise: function(status) {
      var didConsent = this.hasConsented();
      if (didConsent) {
        // User has already consented to cookies
        // Set necessary cookies here
      }
    },
    onStatusChange: function(status, chosenBefore) {
      var didConsent = this.hasConsented();
      if (didConsent) {
        // User has consented to cookies
        // Set necessary cookies here
      } else {
        // User has declined cookies
        // Remove any cookies that were set
      }
    }
  });
});
