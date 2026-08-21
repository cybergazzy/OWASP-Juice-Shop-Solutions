In the previous challenge [API-XSS](../API-only_XSS/screenshots/TerminalOutput.png), you'll notice another path. The 'users' path.

If we send a GET request to that, you'll notice that there is a "role" description which is going to be the backbone of this whole challenge ![GET Request](screenshots/GetUsers.png)

Once we send a POST request for a new user with the role as "admin", ![POST Request](screenshots/PostUser.png)

Challenge Solved! ![Done](screenshots/ScoreBoard.png)

You can also confirm it works by login in with the details ![Login Page](screenshots/LoginPage.png)

And Boom! ![Home Page](screenshots/HomePage.png)
