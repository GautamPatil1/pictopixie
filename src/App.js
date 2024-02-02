import { useState, useEffect } from "react";
import "./App.css";
import Chat from "./components/Chat";
import SearchBox from "./components/Search";
import Navbar from "./components/Navbar";
import { useAuth0 } from "@auth0/auth0-react";

function App() {
  const [content, setContent] = useState([]);
  const server = 'http://localhost:8000';
  const { user, isAuthenticated } = useAuth0();

  useEffect(() => {
    // Fetch content from the server when the component mounts
    const fetchContent = async () => {
      try {
        const response = await fetch(`${server}/user/${user.sub}`) ;
        if (!response.ok) {
          throw new Error('Failed to fetch content');
        }
        const data = await response.json();
        if (data && data.content) {
          setContent(data.content);
        }
      } catch (error) {
        console.error('Error fetching content:', error);
      }
    };

    if (isAuthenticated && user && user.sub) {
      fetchContent();
    }
  }, [isAuthenticated, user]); // Empty dependency array ensures useEffect runs only once on component mount

  const postContent = async (content) => {
    if (isAuthenticated && user && user.sub) {
      try {
        const response = await fetch(`${server}/users/posts`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            userSub: user.sub,
            content: content
          })
        });
    
        if (!response.ok) {
          throw new Error('Failed to post content');
        }
      } catch (error) {
        console.error('Error posting content:', error);
      }
    }
  };

  const updateContent = (newContent) => {
    setContent((prevContent) => [...prevContent, newContent]);
  };

  useEffect(() => {
    if (content.length > 0) {
      postContent(content);
    }
  }, [content, user]); // Trigger postContent whenever content or user changes

  return (
    <div className="App">
      <Navbar />
      <div className="chat-container">
        <Chat
          content={
            "Hi! I'm PictoPixie, your go-to AI buddy for solving problems. Just chat with me, send pics or PDFs, and let's crack those conundrums together!"
          }
        />
        {content.map((item, index) => (
          <Chat key={index} content={item} index={index} />
        ))}
      </div>

      <div className="search-container">
        <SearchBox updateContent={updateContent} />
      </div>
    </div>
  );
}

export default App;

