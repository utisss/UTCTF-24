The number of cookie clicks is tracked with JavaScript and local storage, both of which are controllable by the user.

My solution was to go into my browser's dev tools, go to storage > local storage, edit the amount to "10000000", hit enter, refresh the page, and then click the cookie one more time.
You could also just manufacture the POST request to /click based on the JavaScript to tell the server you have >10,000,000 clicks.

The only hint I'd really give is "how are cookies being tracked"