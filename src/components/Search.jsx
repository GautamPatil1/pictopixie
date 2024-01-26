import React, { useRef, useState } from "react";
import "./Search.css";

const SearchBox = ({updateContent}) => {
  const fileInput = useRef(null);
  const [searchTerm, setSearchTerm] = useState('');
  const serverEndpoint = 'http://localhost:8000'
  const formData = new FormData();

  const handleButtonClick = () => {
    // Trigger the file input when the button is clicked
    document.getElementById("imageInput").click();
  };

  const handleChange = (event) => {
    setSearchTerm(event.target.value)
  }

  const submitPrompt = (event) => {
    event.preventDefault();
    formData.append('prompt', searchTerm)

    fetch(`${serverEndpoint}/upload`, {
      method: "POST",
      body: formData,
    })
      .then(response => response.json())
      .then(data => {
        console.log("Response from server:", data);
        updateContent(data.Result);
      })
      .catch(error => {
        console.error("Error sending file:", error);
      });
    setSearchTerm('');
  }

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
  
    if (selectedFile) {
      // Check the file type
      const fileType = selectedFile.type;
      if (
        fileType === "application/pdf" ||
        fileType === "image/png" ||
        fileType === "image/jpeg" ||
        fileType === "image/jpg"
      ) {
        // Construct form data
        
        formData.append("file", selectedFile);
  
        // Send the file via API
        
      } else {
        alert("Please select a PDF, PNG, JPEG, or JPG file.");
      }
    }
  };
  

  const handlePaperClick = () => {
    fileInput.current.click();
  };

  return (
    <div className="search">
      <button
        type="button"
        className="searchButton"
        onClick={handleButtonClick}
      >
        <i className="fa-solid fa-camera"></i>
      </button>

      <input
        type="file"
        id="imageInput"
        accept="image/*"
        capture="environment"
        onChange={handleFileChange}
        style={{ display: "none" }}
      />

      <input type="text" className="searchTerm" placeholder="Search" value={searchTerm} onChange={handleChange}/>

      <button type="button" className="searchButton" onClick={handlePaperClick}>
        <i className="fa-solid fa-paperclip"></i>
      </button>

      <input
        type="file"
        id="fileInput"
        ref={fileInput}
        style={{ display: "none" }}
        accept=".pdf, .png, .jpeg, .jpg"
        onChange={handleFileChange}
      />

      <button type="submit" className="searchButton" onClick={submitPrompt} >
        <i className="fa-solid fa-bolt"></i>
      </button>
    </div>
  );
};

export default SearchBox;
