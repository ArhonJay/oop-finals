# OOP Finals (Flask hosted by Vercel)

This guide demonstrates how to deploy a Flask 3 application on Vercel, utilizing Serverless Functions with the Python Runtime. Vercel's platform is tailored for serverless architectures, making it perfect for hosting small to medium-scale web applications and APIs without managing servers.

## How it Works

This example uses the Web Server Gateway Interface (WSGI) with Flask to enable handling requests on Vercel with Serverless Functions. WSGI is a specification that serves as a standard interface between web servers and Python web applications or frameworks. It is designed to facilitate a consistent way to deploy Python web applications across various web servers. WSGI ensures that your Flask application can communicate effectively with the Vercel platform.

## Running Locally

```bash
npm i -g vercel
vercel dev
```

Your Flask application is now available at `http://localhost:3000`.
