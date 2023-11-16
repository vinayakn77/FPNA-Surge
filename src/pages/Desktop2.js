import React, { useCallback, useRef, useState } from "react";
import styles from "./Desktop2.module.css";
import { useNavigate } from "react-router-dom";  // Import useNavigate
import axios from "axios";

const Desktop2 = () => {
  const fileInputRef = useRef(null);
  const [selectedFileName, setSelectedFileName] = useState(null);
  const [calculationDone, setCalculationDone] = useState(false); // Track calculation status

  const [isUploading, setIsUploading] = useState(false);
  const [uploadPercentage, setUploadPercentage] = useState(0);
  const [isStepsVisible, setIsStepsVisible] = useState(false);

  const [isUploaded, setIsUploaded] = useState(false);
  const onUploadButtonClick = () => {
    fileInputRef.current.click();
  };
  const navigate = useNavigate();  // Use the useNavigate hook


  // const onNextTextClick = useCallback(() => {
  //   navigate("/desktop-2");
  // }, [navigate]);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      setSelectedFileName(selectedFile.name);
      console.log("Uploading file:", selectedFile.name);
      uploadFile(selectedFile);
    } else {
      setSelectedFileName(null);
      console.log("No file selected");
    }
  };

  const uploadFile = (file) => {
    const formData = new FormData();
    formData.append("file", file);

    setIsUploading(true);

    axios
      .post("http://localhost:5000/uploads", formData, {
        onUploadProgress: (progress) => {
          setUploadPercentage(progress * 100);
        },
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((response) => {
        setIsUploading(false);
        setIsUploaded(true);
      })

      .catch((error) => {
        setIsUploading(false);
        console.error("Error uploading file:", error);
      });
  };

  const onCalculateButtonClick = () => {
    axios
      .get("http://localhost:5000/calculate")
      .then((response) => {
        console.log(response.data);
        setCalculationDone(true);
        setIsStepsVisible(true); // Display steps after calculation
      })
      .catch((error) => {
        console.error("Error calculating:", error);
      });
  };

  const onDownloadButtonClick = () => {
    // Trigger the file download by creating a link and clicking it
    const downloadLink = document.createElement("a");
    downloadLink.href = "http://localhost:5000/outputfiles/Output.csv";
    // downloadLink.href = "https://fpasimulate.azurewebsites.net/outputfiles/Output.csv"
    downloadLink.download = "Output.csv";
    downloadLink.click();
  };

  const onSummarizeClick = useCallback(() => {
    navigate("/desktop-3");
  }, [navigate]);

 

  return (
    <div className={styles.desktop2}>
      <img className={styles.cards1Icon} alt="" src="/cards1@2x.png" />
      <div className={styles.step1UploadThe}>Step-1 Upload the input file</div>
      <div className={styles.desktop2Child} onClick={onUploadButtonClick}/>
      <div
        className={styles.upload}
        onClick={onUploadButtonClick}
      >
        Upload
      </div>
      {isUploading ? (
        <div className={styles.uploadprogress}>
          <div>{uploadPercentage}</div>
          <img src="hourglass.gif" width="40" height="40" />
        </div>
      ) : (
        <></>
      )}
      <form encType="multipart/form-data" style={{ display: "flex" }}>
        <input
          id="fileInput"
          type="file"
          accept=".csv"
          style={{ display: "none" }}
          onChange={handleFileChange}
          ref={fileInputRef}
        />
      </form>

      {isUploaded ? (
        <>
          <div
            className={styles.step2GenerateThe}
            onClick={() => onCalculateButtonClick()}
          >
            Step-2 Generate the three years projection of metrics
          </div>
          <div className={styles.desktop2Item} onClick={() => onCalculateButtonClick()} />
          <div className={styles.generate} onClick={() => onCalculateButtonClick()}>Generate</div>
        </>
      ) : (
        <></>
      )}

      {isStepsVisible ? (
        <>
          <div className={styles.step3DownloadThe}>
            Step-3 Download the output file
          </div>
          <div className={styles.desktop2Inner} onClick={onDownloadButtonClick} />
          <div className={styles.download} onClick={onDownloadButtonClick}>Download</div>
          <div className={styles.step4CreateThe}>
            Step-4 Create the summary table
          </div>
          <div className={styles.rectangleDiv} />
          <div className={styles.summarize} onClick={onSummarizeClick}>Summarize</div>
        </>
      ) : (
        <></>
      )}
    </div>
  );
};

export default Desktop2;
