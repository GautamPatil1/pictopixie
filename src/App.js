import { useState } from "react";
import "./App.css";
import Chat from "./components/Chat";
import SearchBox from "./components/Search";
import Navbar from "./components/Navbar";
function App() {
  const [content, setContent] = useState([]);

  const updateContent = (newContent) => {
    setContent((prevContent) => [...prevContent, newContent]);
  };

  return (
    <div
      className="App"
      style={{
        display: "flex",
        flexDirection: "column",
        height: "100vh",
        backgroundColor: "#181818",
      }}
    >
      <Navbar />
      <div className="chat-container">
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
