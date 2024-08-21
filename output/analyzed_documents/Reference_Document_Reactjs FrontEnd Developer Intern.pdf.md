# Detailed Reference Document for ReactJS Frontend Developer Internship Assignment

## 1. Overview

Welcome to the ReactJS Frontend Developer internship assignment. This document provides a comprehensive guide to help you create a functional and aesthetically pleasing admin dashboard for a social media application. The primary objective is to build a dashboard that includes a home page and pages to list users and posts.

### Expected Outcomes:
- An admin dashboard with the following key components:
  - Home Page with KPIs
  - Users Listing Page
  - Posts Listing Page
- Navigation bar on the left of all pages
- Controls for user and post management
- A dummy dataset for demonstration
- A dummy login page 

## 2. Step-by-Step Instructions

### 2.1 Setting Up the Project

1. **Install Node.js and npm**:
   - Make sure you have Node.js and npm installed. You can download it [here](https://nodejs.org/).
   - Verify installation using:
     ```sh
     node -v
     npm -v
     ```

2. **Initialize a React Project**:
   - Create a new directory for your project and navigate into it:
     ```sh
     mkdir admin-dashboard
     cd admin-dashboard
     ```
   - Initialize a new React project (you can choose `create-react-app` or `Next.js`):
     ```sh
     npx create-react-app my-admin-dashboard
     cd my-admin-dashboard
     ```

3. **Install Required Dependencies**:
   - Install additional libraries if necessary (e.g., react-router-dom for routing, Material-UI or Ant Design for UI components):
     ```sh
     npm install react-router-dom @material-ui/core @material-ui/icons
     ```

### 2.2 Building the Admin Dashboard

1. **Set Up Routing**:
   - Create basic routes for the Home Page, Users Listing Page, and Posts Listing Page:
     ```jsx
     import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
     import HomePage from './components/HomePage';
     import UsersPage from './components/UsersPage';
     import PostsPage from './components/PostsPage';

     function App() {
       return (
         <Router>
           <Switch>
             <Route exact path="/" component={HomePage} />
             <Route path="/users" component={UsersPage} />
             <Route path="/posts" component={PostsPage} />
           </Switch>
         </Router>
       );
     }
     export default App;
     ```

2. **Create Navigation Bar**:
   - Implement a sidebar for navigation:
     ```jsx
     import { Link } from 'react-router-dom';
     // Add your styles here or use a library like Material-UI

     function Sidebar() {
       return (
         <div className="sidebar">
           <Link to="/">Home</Link>
           <Link to="/users">Users</Link>
           <Link to="/posts">Posts</Link>
         </div>
       );
     }
     ```

3. **Design the Home Page**:
   - HomePage Component:
     ```jsx
     function HomePage() {
       return (
         <div>
           <h1>Home Page</h1>
           <div className="kpi-container">
             <div className="kpi-box">Total Users</div>
             <div className="kpi-box">Total Posts</div>
             <div className="kpi-box">Users active in the last 24 hours</div>
             <div className="kpi-box">Posts published in the last 24 hours</div>
           </div>
         </div>
       );
     }
     export default HomePage;
     ```

4. **Create Users Listing Page**:
   - UsersPage Component:
     ```jsx
     function UsersPage() {
       // Dummy data
       const users = [{ user_id: 1, username: 'user1', name: 'User One', email: 'user1@example.com' }];
       
       return (
         <div>
           <h1>Users Listing</h1>
           <div className="kpi-container">
             <div className="kpi-box">Total Users</div>
             <div className="kpi-box">Users active in the last 24 hours</div>
           </div>
           <table>
             <thead>
               <tr>
                 <th>User ID</th>
                 <th>Username</th>
                 <th>Name</th>
                 <th>Email</th>
                 <th>Actions</th>
               </tr>
             </thead>
             <tbody>
               {users.map(user => (
                 <tr key={user.user_id}>
                   <td>{user.user_id}</td>
                   <td>{user.username}</td>
                   <td>{user.name}</td>
                   <td>{user.email}</td>
                   <td>
                     <button>Edit</button>
                     <button>Ban</button>
                   </td>
                 </tr>
               ))}
             </tbody>
           </table>
         </div>
       );
     }
     export default UsersPage;
     ```

5. **Create Posts Listing Page**:
   - PostsPage Component:
     ```jsx
     function PostsPage() {
       // Dummy data
       const posts = [{ post_id: 1, post_caption: 'Post One', media_url: 'http://example.com/media1.jpg' }];
       
       return (
         <div>
           <h1>Posts Listing</h1>
           <div className="kpi-container">
             <div className="kpi-box">Total Posts</div>
             <div className="kpi-box">Posts published in the last 24 hours</div>
           </div>
           <table>
             <thead>
               <tr>
                 <th>Post ID</th>
                 <th>Post Caption</th>
                 <th>Media URL</th>
                 <th>Actions</th>
               </tr>
             </thead>
             <tbody>
               {posts.map(post => (
                 <tr key={post.post_id}>
                   <td>{post.post_id}</td>
                   <td>{post.post_caption}</td>
                   <td>{post.media_url}</td>
                   <td>
                     <button>Delete</button>
                     <button>Hide</button>
                   </td>
                 </tr>
               ))}
             </tbody>
           </table>
         </div>
       );
     }
     export default PostsPage;
     ```

6. **Create Dummy Dataset**:
   - Use JavaScript arrays or import JSON files with dummy data for users and posts.

7. **Set Up Dummy Login Page**:
   - Simple login component:
     ```jsx
     import { useState } from 'react';
     import { useHistory } from 'react-router-dom';

     function Login() {
       const [email, setEmail] = useState('');
       const [password, setPassword] = useState('');
       const history = useHistory();

       const handleLogin = () => {
         if (email && password) {
           history.push('/');
         }
       };

       return (
         <div>
           <h1>Login</h1>
           <div>
             <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
             <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
             <button onClick={handleLogin}>Log In</button>
           </div>
         </div>
       );
     }
     export default Login;
     ```

### 2.3 Additional Features and Finishing Touches

1. **Styled Components / CSS-in-JS**:
   - Use libraries like styled-components or CSS-in-JS for better maintainability of styles.

2. **Form Validation**:
   - Add validation to the dummy login form to simulate a real login environment.

## 3. Best Practices

- **Code Organization**: Keep your file structure organized. Create separate folders for components, pages, and assets.
- **Reusable Components**: Make components reusable whenever possible, like the KPI box and table rows.
- **Error Handling**: Implement error handling mechanisms to deal with unexpected behavior.
- **Comments and Documentation**: Comment your code and ensure your code is readable and well-documented.

## 4. Submission Guidelines

- **Code**: Share the complete code, excluding the `node_modules` folder.
- **README File**: Include a README file with instructions for setting up and testing the app.
- **Video Recording**: Provide a 1-2 minute video demonstrating the working dashboard.
- **Screenshots**: Add screenshots of the dashboard in the README file.
- **ZIP File**: Package the code, README file, and video recording into a ZIP file.
- **Upload**: Upload the ZIP file to Google Drive and share the public access link.

## 5. FAQ Section

### Q: How do I start the development server?
A: Navigate to your project directory and run `npm start` or `yarn start`.

### Q: My components are not rendering properly. What could be wrong?
A: Check if you have correctly imported and used the components in your routes and navigation.

### Q: How do I handle state in my application?
A: Use React hooks like `useState` and `useEffect` to manage state.

### Q: What should I do if I encounter dependency issues?
A: Make sure you are using compatible versions of dependencies. Check the official documentation for guidance.

### Q: How can I paginate the list views?
A: Use libraries like `react-paginate` or build a simple pagination component manually using state.

We hope this document serves as a useful guide for completing the assignment. Good luck!
