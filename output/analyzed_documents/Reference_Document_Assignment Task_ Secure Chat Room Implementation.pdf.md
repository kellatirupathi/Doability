# Secure Chat Room Implementation: Reference Document

## 1. Overview

### Introduction
This document outlines the steps and procedures for implementing a secure chat room system as part of the LeadMint Backend Assessment. The assignment requires creating a robust and secure chat room application using JavaScript, Node.js, MySQL, and Express. The key features include user registration and authentication, chat room creation, inviting participants, real-time messaging, profile viewing, friend requests, and stringent security measures.

### Objectives
- **User Authentication**: Secure user registration and login using JWT.
- **Chat Room Management**: Prime members can create chat rooms and invite participants.
- **Interactive Communication**: Real-time exchange of messages within chat rooms using WebSocket.
- **Profile and Friend Features**: Users can view profiles and send friend requests.
- **Security**: Implement strong security practices to protect user data.
  
### Expected Outcomes
A fully operational chat room system that ensures secure communication and user management, robust error handling, and well-documented code.

---

## 2. Step-by-Step Instructions

### Prerequisites
- **Node.js**
- **MySQL database**
- **Git for version control**

### Step 1: Setting Up the Project

1. **Initialize a New Node Project**
    ```bash
    mkdir secure-chat-room
    cd secure-chat-room
    npm init -y
    ```

2. **Install Required Packages**
    ```bash
    npm install express mysql jwt-simple bcryptjs body-parser nodemon websocket dotenv
    ```

3. **Set Up Project Structure**
    ```
    secure-chat-room/
    ├── config/
    │   └── db.js
    ├── controllers/
    ├── models/
    ├── routes/
    ├── middleware/
    ├── .env
    ├── app.js
    ├── package.json
    └── README.md
    ```

### Step 2: Setting Up MySQL Database

1. **Create Database and Tables**
    - Create a database named `secure_chat`.
    - Implement the required tables (users, chat_rooms, messages, friend_requests) as per the following schema:
    ```sql
    CREATE TABLE users (
        userId INT PRIMARY KEY AUTO_INCREMENT,
        deviceId VARCHAR(255) NOT NULL,
        name VARCHAR(255) NOT NULL,
        phone VARCHAR(20) NOT NULL,
        availCoins INT DEFAULT 0,
        password VARCHAR(255) NOT NULL,
        isPrime BOOLEAN DEFAULT FALSE,
        UNIQUE(phone)
    );

    CREATE TABLE chat_rooms (
        roomId INT PRIMARY KEY AUTO_INCREMENT,
        userId INT NOT NULL,
        roomName VARCHAR(255) NOT NULL,
        roomPassword VARCHAR(255),
        CONSTRAINT fk_user FOREIGN KEY(userId) REFERENCES users(userId)
    );

    CREATE TABLE messages (
        messageId INT PRIMARY KEY AUTO_INCREMENT,
        roomId INT NOT NULL,
        userId INT NOT NULL,
        content TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(roomId) REFERENCES chat_rooms(roomId),
        FOREIGN KEY(userId) REFERENCES users(userId)
    );

    CREATE TABLE friend_requests (
        requestId INT PRIMARY KEY AUTO_INCREMENT,
        senderId INT NOT NULL,
        receiverId INT NOT NULL,
        status VARCHAR(50) DEFAULT 'pending',
        FOREIGN KEY(senderId) REFERENCES users(userId),
        FOREIGN KEY(receiverId) REFERENCES users(userId)
    );
    ```

### Step 3: Configuration

1. **Database Configuration**
    - Create a configuration file for database connection `config/db.js`:
    ```javascript
    const mysql = require('mysql');
    const connection = mysql.createConnection({
        host: process.env.DB_HOST,
        user: process.env.DB_USER,
        password: process.env.DB_PASS,
        database: process.env.DB_NAME,
    });

    connection.connect(err => {
        if (err) throw err;
        console.log('Database connected!');
    });

    module.exports = connection;
    ```

2. **Environment Variables**
    - Create a `.env` file to store environment variables:
    ```plaintext
    DB_HOST=localhost
    DB_USER=root
    DB_PASS=yourpassword
    DB_NAME=secure_chat
    JWT_SECRET=your_jwt_secret
    ```

### Step 4: User Registration and Authentication

1. **User Model and Controller**
    - Create `models/userModel.js` and `controllers/authController.js` for handling user operations:
    ```javascript
    // models/userModel.js
    const connection = require('../config/db');
    const bcrypt = require('bcryptjs');

    async function saveUser(user) {
        const hashedPassword = await bcrypt.hash(user.password, 10);
        const query = `INSERT INTO users (deviceId, name, phone, availCoins, password) VALUES (?, ?, ?, ?, ?)`;
        return new Promise((resolve, reject) => {
            connection.query(query, [user.deviceId, user.name, user.phone, user.availCoins, hashedPassword], (err, result) => {
                if (err) reject(err);
                resolve(result);
            });
        });
    }

    module.exports = {
        saveUser,
    };
    ```

    ```javascript
    // controllers/authController.js
    const jwt = require('jwt-simple');
    const bcrypt = require('bcryptjs');
    const userModel = require('../models/userModel');
    const connection = require('../config/db');

    async function register(req, res) {
        const { deviceId, name, phone, availCoins, password } = req.body;
        try {
            const result = await userModel.saveUser({ deviceId, name, phone, availCoins, password });
            res.status(201).json({ message: 'User registered!', data: result });
        } catch (err) {
            res.status(500).json({ error: err.message });
        }
    }

    async function login(req, res) {
        const { phone, password } = req.body;
        const query = `SELECT * FROM users WHERE phone = ?`;
        
        connection.query(query, [phone], async (err, results) => {
            if (err) return res.status(500).json({ error: err.message });
            if (results.length === 0) return res.status(404).json({ message: 'User not found!' });

            const user = results[0];
            const isValidPassword = await bcrypt.compare(password, user.password);
            if (!isValidPassword) return res.status(401).json({ message: 'Invalid credentials!' });

            const token = jwt.encode({ userId: user.userId }, process.env.JWT_SECRET);
            res.status(200).json({ token, userId: user.userId, isPrime: user.isPrime });
        });
    }

    module.exports = {
        register,
        login,
    };
    ```

2. **Routes for Authentication**
    - Create a routes file `routes/authRoutes.js`:
    ```javascript
    const express = require('express');
    const authController = require('../controllers/authController');
    const router = express.Router();

    router.post('/register', authController.register);
    router.post('/login', authController.login);

    module.exports = router;
    ```

### Step 5: Securing Endpoints and Adding Features

1. **Middleware for Authentication and Authorization**
    - Create `middleware/authMiddleware.js`:
    ```javascript
    const jwt = require('jwt-simple');
    
    function authenticate(req, res, next) {
        const token = req.headers['authorization'];
        if (!token) return res.status(401).json({ message: 'Unauthorized' });

        try {
            const decoded = jwt.decode(token, process.env.JWT_SECRET);
            req.userId = decoded.userId;
            next();
        } catch (err) {
            res.status(401).json({ message: 'Invalid Token' });
        }
    }

    async function authorize(req, res, next) {
        // Add logic to check if the user is a prime member
        const userId = req.userId;
        // Fetch user by userId and check if isPrime==true
        next();
    }

    module.exports = {
        authenticate,
        authorize,
    };
    ```

2. **Chat Room Creation and Management**
    - Create `models/chatRoomModel.js` and `controllers/chatRoomController.js`:
    ```javascript
    // models/chatRoomModel.js
    const connection = require('../config/db');

    function createRoom(userId, roomName, roomPassword) {
        const query = `INSERT INTO chat_rooms (userId, roomName, roomPassword) VALUES (?, ?, ?)`;
        return new Promise((resolve, reject) => {
            connection.query(query, [userId, roomName, roomPassword], (err, result) => {
                if (err) reject(err);
                resolve(result);
            });
        });
    }

    module.exports = {
        createRoom,
    };
    ```

    ```javascript
    // controllers/chatRoomController.js
    const chatRoomModel = require('../models/chatRoomModel');
    
    async function createChatRoom(req, res) {
        const { roomName, roomPassword } = req.body;
        const userId = req.userId;
        
        try {
            const result = await chatRoomModel.createRoom(userId, roomName, roomPassword);
            res.status(201).json({ message: 'Chat room created!', data: result });
        } catch (err) {
            res.status(500).json({ error: err.message });
        }
    }

    module.exports = {
        createChatRoom,
    };
    ```

3. **Routes for Chat Room Management**
    - Create a routes file `routes/chatRoomRoutes.js`:
    ```javascript
    const express = require('express');
    const chatRoomController = require('../controllers/chatRoomController');
    const authMiddleware = require('../middleware/authMiddleware');
    const router = express.Router();

    router.post('/create', authMiddleware.authenticate, authMiddleware.authorize, chatRoomController.createChatRoom);

    module.exports = router;
    ```

### Step 6: Real-Time Messaging

1. **Implement WebSocket for Real-Time Messaging**
    - Configure WebSocket in `app.js`:
    ```javascript
    const express = require('express');
    const WebSocket = require('ws');
    const app = express();
    const server = require('http').createServer(app);
    const wss = new WebSocket.Server({ server });

    wss.on('connection', (ws) => {
        ws.on('message', (message) => {
            // Broadcast message to all clients
            wss.clients.forEach((client) => {
                if (client !== ws && client.readyState === WebSocket.OPEN) {
                    client.send(message);
                }
            });
        });
    });

    server.listen(3000, () => {
        console.log('Server is listening on port 3000');
    });
    ```

### Step 7: Profile Viewing, Friend Requests, and Other Features

1. **Profile Viewing**
    - Create `models/profileModel.js` and `controllers/profileController.js`:
    ```javascript
    // models/profileModel.js
    const connection = require('../config/db');

    function getUserProfile(userId) {
        const query = `SELECT * FROM users WHERE userId = ?`;
        return new Promise((resolve, reject) => {
            connection.query(query, [userId], (err, results) => {
                if (err) reject(err);
                resolve(results[0]);
            });
        });
    }

    module.exports = {
        getUserProfile,
    };
    ```

    ```javascript
    // controllers/profileController.js
    const profileModel = require('../models/profileModel');

    async function getProfile(req, res) {
        const userId = req.params.userId;

        try {
            const user = await profileModel.getUserProfile(userId);
            res.status(200).json(user);
        } catch (err) {
            res.status(500).json({ error: err.message });
        }
    }

    module.exports = {
        getProfile,
    };
    ```

2. **Friend Requests**
    - Create `models/friendRequestModel.js` and `controllers/friendRequestController.js`:
    ```javascript
    // models/friendRequestModel.js
    const connection = require('../config/db');

    function sendFriendRequest(senderId, receiverId) {
        const query = `INSERT INTO friend_requests (senderId, receiverId) VALUES (?, ?)`;
        return new Promise((resolve, reject) => {
            connection.query(query, [senderId, receiverId], (err, result) => {
                if (err) reject(err);
                resolve(result);
            });
        });
    }

    module.exports = {
        sendFriendRequest,
    };
    ```

    ```javascript
    // controllers/friendRequestController.js
    const friendRequestModel = require('../models/friendRequestModel');

    async function sendRequest(req, res) {
        const { receiverId } = req.body;
        const senderId = req.userId;

        try {
            const result = await friendRequestModel.sendFriendRequest(senderId, receiverId);
            res.status(201).json({ message: 'Friend request sent!', data: result });
        } catch (err) {
            res.status(500).json({ error: err.message });
        }
    }

    module.exports = {
        sendRequest,
    };
    ```

3. **Routes for Profiles and Friend Requests**
    - Create routes files `routes/profileRoutes.js` and `routes/friendRequestRoutes.js`:
    ```javascript
    // routes/profileRoutes.js
    const express = require('express');
    const profileController = require('../controllers/profileController');
    const authMiddleware = require('../middleware/authMiddleware');
    const router = express.Router();

    router.get('/:userId', authMiddleware.authenticate, profileController.getProfile);

    module.exports = router;
    ```

    ```javascript
    // routes/friendRequestRoutes.js
    const express = require('express');
    const friendRequestController = require('../controllers/friendRequestController');
    const authMiddleware = require('../middleware/authMiddleware');
    const router = express.Router();

    router.post('/', authMiddleware.authenticate, friendRequestController.sendRequest);

    module.exports = router;
    ```

### Step 8: Error Handling and Validation

1. **Implement Robust Error Handling and Validation**
    - Add appropriate error handling in all controllers and middleware.
    - Ensure input validation using middleware or libraries like `express-validator`.

### Step 9: Version Control and Project Submission

1. **Initialize Git Repository**
    ```bash
    git init
    git add .
    git commit -m "Initial commit"
    ```
    
2. **Push to GitHub**
    - Create a repository on GitHub and push your code:
    ```bash
    git remote add origin https://github.com/yourusername/secure-chat-room.git
    git push -u origin main
    ```

3. **Document API Endpoints in README**
    ```markdown
    # Secure Chat Room API

    ## Endpoints

    ### User Authentication
    - **POST /register**: Register a new user.
    - **POST /login**: Login a user.

    ### Chat Rooms
    - **POST /create**: Create a new chat room.
    ```

4. **Submission Guidelines**
    - Provide a GitHub repository link with the complete code.
    - Include a README file with instructions on setting up and running the application.
    - Share database schema in a separate `.sql` file.
    - Clearly document API endpoints, expected request and response formats, and any additional features.

---

## 3. Best Practices

### Tips for Efficient Completion

1. **Follow Coding Standards**: Use proper naming conventions and maintain a consistent coding style.
2. **Modular Code Design**: Structure your code logically with clear separation of concerns.
3. **Thorough Testing**: Test all endpoints and features rigorously to ensure they work as expected.
4. **Error Handling**: Handle errors gracefully and provide meaningful feedback to the client.
5. **Security Measures**: Implement all recommended security practices, especially for authentication and data protection.

### Avoiding Common Pitfalls

1. **Incomplete Features**: Ensure all the specified features are implemented.
2. **Lack of Documentation**: Properly document your code and API endpoints.
3. **Poor Database Schema**: Design the database schema carefully to accommodate all requirements efficiently.
4. **Ignoring Validation**: Validate all user inputs to prevent invalid data entry.

---

## 4. Submission Guidelines

### How to Submit

- **GitHub Repository**:
  - Push your complete code to a GitHub repository.
  - Include a README file with detailed setup and run instructions.
  - Provide the database schema in a `.sql` file.
  - Clearly document API endpoints and expected request/response formats.

### Where to Submit

- **Submission Deadline**: 6th June, 2024, till 7 P.M.
- **Submit to**: 
  - **Primary**: rishav@leadmint.io
  - **CC**: shabaj@leadmint.io

---

## 5. FAQ Section

### Common Questions

1. **Q: How do I test the API endpoints?**
   - **A**: Use tools like Postman to send requests to the API and validate responses.

2. **Q: How do I secure sensitive information?**
   - **A**: Use environment variables for sensitive information and ensure tokens are properly managed.

3. **Q: What should I do if I encounter a database error?**
   - **A**: Ensure your database connection settings are correct and review your SQL queries for syntax errors.

4. **Q: How do I handle password security?**
   - **A**: Store passwords securely by hashing them using bcrypt before saving to the database.

5. **Q: What if I need more time for submission?**
   - **A**: Contact rishav@leadmint.io or shabaj@leadmint.io for any concerns about the deadline.

---

This detailed reference document should guide you effectively through the process of developing a secure chat room system, ensuring successful completion of the assignment. Good luck!
