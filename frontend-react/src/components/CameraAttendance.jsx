import { useRef, useState } from "react";
import "./CameraAttendance.css";

const API = "http://127.0.0.1:8000/mark-attendance";

export default function CameraAttendance({ onMarked }) {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);
  const intervalRef = useRef(null);

  const [status, setStatus] = useState("Idle");
  const [marked, setMarked] = useState(null);

  const start = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    streamRef.current = stream;
    videoRef.current.srcObject = stream;
    setStatus("Scanning...");
    capture();
  };

  const capture = () => {
    intervalRef.current = setInterval(async () => {
      const ctx = canvasRef.current.getContext("2d");
      canvasRef.current.width = videoRef.current.videoWidth;
      canvasRef.current.height = videoRef.current.videoHeight;
      ctx.drawImage(videoRef.current, 0, 0);

      const frame = canvasRef.current.toDataURL("image/jpeg");

      const res = await fetch(API, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          frame,
          timestamp: new Date().toISOString(),
        }),
      });

      const data = await res.json();

      if (data.marked?.length) {
        setMarked(data.marked[0]);
        setStatus("Attendance Marked");
        stop();
        onMarked?.();
      }
    }, 2000);
  };

  const stop = () => {
    clearInterval(intervalRef.current);
    streamRef.current?.getTracks().forEach(t => t.stop());
  };

  return (
    <div className="camera-box">
      <video ref={videoRef} autoPlay muted />
      <canvas ref={canvasRef} hidden />

      <p>Status: {status}</p>
      {marked && <p className="success">Marked: {marked}</p>}

      <button onClick={start}>Start Attendance</button>
    </div>
  );
}
