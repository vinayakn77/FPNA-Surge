import { useCallback } from "react";
import { useNavigate } from "react-router-dom";
import styles from "./Desktop1.module.css";

const Desktop1 = () => {
  const navigate = useNavigate();

  const onRectangleClick = useCallback(() => {
    navigate("/desktop-2");
  }, [navigate]);

  return (
    <div className={styles.desktop1}>
      <img className={styles.cards1Icon} alt="" src="/cards1@2x.png" />
      <div className={styles.financialSimulationUsing}>
        Financial Simulation using Credit Card Data
      </div>
      <div className={styles.step1UploadTheContainer}>
        <p className={styles.step1UploadThe}>
          Step-1 Upload the base year input file
        </p>
        <p className={styles.step1UploadThe}>
          Step-2 Generate the three years projection of metrics
        </p>
        <p className={styles.step1UploadThe}>
          Step-3 Download the projections output file
        </p>
        <p className={styles.step1UploadThe}>Step-4 Create the summary table</p>
        <p className={styles.step1UploadThe}>Step-5 Simulate Scenarios</p>
        <p className={styles.step1UploadThe}>Step-6 Visualize</p>
      </div>
      <div className={styles.steps}>Steps :</div>
      <div className={styles.desktop1Child} onClick={onRectangleClick} />
      <div className={styles.getStarted} onClick={onRectangleClick}>Get Started</div>
      
      <div className={styles.loremIpsumDolorContainer}>
        <p className={styles.step1UploadThe}>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
          eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad
          minim veniam, quis nostrud exercitation ullamco laboris nisi ut
          aliquip ex ea commodo consequat. Duis aute irure dolor in
          reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
          pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
          culpa qui officia deserunt mollit anim id est laborum.c
        </p>
      </div>
    </div>
  );
};

export default Desktop1;

