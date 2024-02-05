import React, { useEffect, useRef } from "react";
import { marked } from "marked";
import { useAuth0 } from "@auth0/auth0-react";
import './Chat.css';

const Chat = (props) => {
  const {user} = useAuth0();
  const containerRef = useRef(null);
  const htmlString = props.content ? marked(props.content) : "";

  const scrollToBottom = () => {
    containerRef.current.scrollIntoView({
      behavior: "smooth",
      block: "end",
      inline: "nearest",
    });
  };

  useEffect(() => {
    scrollToBottom();
  }, [props.content]);

  return (
    <div
      className={`Chat ${ props.index % 2 == 0 ? 'even' : 'odd'}`}
      ref={containerRef}
    >
      <p className="chat-inside">
        {props.index % 2 == 0 ? (
        user ? <img className="user-picture" src={user.picture}/> : <i className="fa-solid fa-user"></i>
        )
        : 
        (
        <img className="robot-icon-chat" src={process.env.PUBLIC_URL + '/bot.png'} alt="robot" />
        )
        }
        <span dangerouslySetInnerHTML={{ __html: htmlString }} />
      </p>
    </div>
  );
};

export default Chat;
