import React, { useState } from "react";
import axios from "axios";
import API_BASE_URL from "../config";

const HomePage = () => {
  const [file, setFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [result, setResult] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select an image to upload.");
      return;
    }

    setIsUploading(true);
    const formData = new FormData();
    formData.append("image", file);

    try {
      const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setResult(response.data);
    } catch (error) {
      console.error("Error uploading image:", error);
      alert("Failed to process the image. Please try again.");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="container">
      <h1>Prostate Cancer Detection</h1>
      <input type="file" onChange={handleFileChange} accept="image/*" />
      <button disabled={isUploading} onClick={handleUpload}>
        {isUploading ? "Processing..." : "Upload and Analyze"}
      </button>

      {result && (
        <div>
          <h3>Results:</h3>
          <p>Classification: {result.label}</p>
          <div>
            <h4>Uploaded Image:</h4>
            <img src={result.originalImage} alt="Uploaded" style={{ width: "300px" }} />
          </div>
          <div>
            <h4>Highlighted Cancer Region:</h4>
            <img src={result.cancerOverlay} alt="Cancer Highlight" style={{ width: "300px" }} />
          </div>
        </div>
      )}
    </div>
  );
};

export default HomePage;
