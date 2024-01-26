import React from 'react';
import {marked} from 'marked';

const Chat = (props) => {
    const htmlContent = props.content
    const htmlString = props.content ? marked(props.content) : '';
    return (
        <div className="Chat"
        style={{
            backgroundColor: '#cfebb6',
            border: '1px solid black',
            width: 'auto',
            overflow: 'visible',
            wordWrap: 'break-word',
            margin: '1rem'
            }}
        >
        <p>
            <div dangerouslySetInnerHTML={{ __html: htmlString }} />
        </p>
        </div>
    );
}

export default Chat;