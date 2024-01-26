import { useState } from "react";
import "./App.css";
import Chat from "./components/Chat";
import SearchBox from "./components/Search";
function App() {
  const [content, setContent] = useState("");

  const updateContent = (newContent) => {
    setContent(newContent);
  }

  return (
    <div
      className="App"
      style={{
        display: "flex",
        flexDirection: "column",
        // justifyContent: "flex-end",
        height: "100vh",
        backgroundColor: "white",
      }}
    >
      <Chat content={"loremipsumloremipsumloremipsumloremipsumloremipsumloremipsumloremipsumloremipsumloremipsumloremipsumloremipsumloremipsumloremipsumloremipsumloremipsumloremipsumloremipsumloremipsumloremipsumloremipsumloremipsumloremipsumloremipsum"} />
      <Chat content={content} />
      <Chat content={content} />
      <SearchBox updateContent={updateContent} />
    </div>
  );
}

export default App;
