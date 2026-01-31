import { useEffect, useState } from "react";
import "./App.css";
import CameraAttendance from "./components/CameraAttendance";

const API_URL = "http://127.0.0.1:8000/attendance";

export default function App() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(false);

  const loadAttendance = async () => {
    setLoading(true);
    const res = await fetch(API_URL);
    const data = await res.json();
    setRecords(Array.isArray(data) ? data : []);
    setLoading(false);
  };

  useEffect(() => {
    loadAttendance();
  }, []);

  return (
    <div className="app">
      <header className="header">
        <h1>Smart Attendance System</h1>
        <p>Real-time Face Recognition Dashboard</p>
      </header>

      <div className="dashboard">
        <div className="card camera-card">
          <h2>Live Camera</h2>
          <CameraAttendance onMarked={loadAttendance} />
        </div>

        <div className="card stats-card">
          <h2>Stats</h2>
          <p>Total Records: <strong>{records.length}</strong></p>
          <button onClick={loadAttendance}>
            {loading ? "Refreshing..." : "Refresh Records"}
          </button>
        </div>
      </div>

      <div className="card table-card">
        <h2>Attendance Records</h2>

        {records.length === 0 ? (
          <p className="empty">No attendance records</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>#</th>
                <th>Name</th>
                <th>Date</th>
                <th>Time</th>
              </tr>
            </thead>
            <tbody>
              {records.map((r, i) => (
                <tr key={i}>
                  <td>{i + 1}</td>
                  <td>{r.name}</td>
                  <td>{r.date}</td>
                  <td>{r.time}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
