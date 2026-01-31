# Quick Reference: Camera Component

## File Structure
```
frontend-react/
├── src/
│   ├── components/
│   │   ├── CameraAttendance.jsx         (NEW - Main component)
│   │   └── CameraAttendance.css         (NEW - Styles)
│   ├── App.jsx                           (MODIFIED - Integration)
│   └── App.css                           (Unchanged)
├── CAMERA_COMPONENT_DOCS.md             (NEW - Full documentation)
└── IMPLEMENTATION_SUMMARY.md            (NEW - Summary)
```

---

## Component Usage
```jsx
import CameraAttendance from "./components/CameraAttendance";

function App() {
  return (
    <div>
      <CameraAttendance />
    </div>
  );
}
```

---

## How to Test

### 1. Start Frontend
```bash
cd frontend-react
npm run dev
```

### 2. Open Browser
```
http://localhost:5173
```

### 3. Click "Start Attendance"
- Browser asks for camera permission
- Grant permission
- Live video appears

### 4. Check Console
```
F12 → Console tab → Look for "Backend Response:"
```

### 5. Click "Stop Attendance"
- Camera stops
- Status updates

---

## Key Endpoints

### Backend Expects
```
POST http://127.0.0.1:8000/mark-attendance
Content-Type: application/json

{
  "frame": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
  "timestamp": "2026-01-31T10:30:45.123Z"
}
```

### Backend Response (Example)
```json
{
  "status": "ok",
  "detected": true,
  "name": "Rohan",
  "message": "Attendance marked successfully"
}
```

---

## State Flow

```
User Interface States:

1. READY (Initial)
   - Start: enabled
   - Stop: disabled
   - Video: empty placeholder

2. REQUESTING (After click Start)
   - Status: "Requesting camera permission..."
   - Both buttons: disabled

3. ACTIVE (Camera On)
   - Start: disabled
   - Stop: enabled
   - Video: live stream
   - Status: "Camera Active - Starting frame capture..."

4. SENDING (Every 2 seconds)
   - Status: "Sending frame..."
   - Frame counter: increments

5. STOPPED (After click Stop)
   - Start: enabled
   - Stop: disabled
   - Video: placeholder
   - Status: "Attendance stopped"

6. ERROR (Any error)
   - Red alert box
   - Start: enabled (can retry)
   - Stop: disabled
```

---

## Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "Camera permission denied" | User clicked Deny | Check browser settings |
| "No camera found" | Device has no camera | Plug in camera |
| "Camera API not supported" | Old browser | Use Chrome/Firefox |
| "Backend returned status 500" | Backend error | Check backend logs |
| "Failed to connect to backend" | FastAPI not running | Start FastAPI server |

---

## Code Highlights

### Start Camera
```javascript
const stream = await navigator.mediaDevices.getUserMedia({
  video: { width: { ideal: 640 }, height: { ideal: 480 } },
  audio: false,
});
videoRef.current.srcObject = stream;
```

### Capture Frame
```javascript
const ctx = canvasRef.current.getContext("2d");
ctx.drawImage(videoRef.current, 0, 0);
const frameBase64 = canvasRef.current.toDataURL("image/jpeg", 0.8);
```

### Send to Backend
```javascript
const response = await fetch("http://127.0.0.1:8000/mark-attendance", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    frame: frameBase64,
    timestamp: new Date().toISOString(),
  }),
});
```

### Stop Camera
```javascript
streamRef.current.getTracks().forEach((track) => track.stop());
videoRef.current.srcObject = null;
clearInterval(intervalRef.current);
```

---

## Browser DevTools Debugging

### Check API Requests
```
DevTools → Network tab → Filter: XHR
Look for POST requests to /mark-attendance
```

### Check Console Logs
```
DevTools → Console tab
Look for:
- "API Response: {...}"
- "Backend Response: {...}"
- "Camera Error: ..."
- "Frame capture error: ..."
```

### Monitor Performance
```
DevTools → Performance tab
- Record while camera is active
- Check CPU usage
- Check memory usage
```

---

## Component Props
**None** - Component is self-contained and manages its own state.

---

## Component Exports
```javascript
export default CameraAttendance;
// No named exports
```

---

## Styling Classes

### Main Container
```css
.camera-container      /* Outer wrapper */
.camera-card           /* Main card */
```

### Video Section
```css
.video-container       /* Video wrapper */
.video-preview         /* Video element */
.video-placeholder     /* Empty state */
```

### Status & Buttons
```css
.status-bar            /* Status display */
.button-group          /* Button container */
.btn                   /* Base button */
.btn-start             /* Start button */
.btn-stop              /* Stop button */
```

### Feedback
```css
.error-alert           /* Error message */
.frame-counter         /* Frame count display */
.helper-text           /* Instructions */
```

---

## Performance Tips

✅ DO:
- Start camera only when needed
- Use 2-second interval to avoid overload
- Compress frames to 80% JPEG quality
- Stop camera when done (cleanup)

❌ DON'T:
- Send frames every frame (~30/sec) - too much bandwidth
- Store all frames in memory
- Leave camera running in background
- Send high-quality images - increases latency

---

## Security Notes

⚠️ Current Implementation:
- No authentication (local dev only)
- HTTP not HTTPS (local dev only)
- No API rate limiting (local dev only)

🔒 For Production:
- Add authentication token
- Use HTTPS/WSS
- Implement rate limiting on backend
- Validate frame size on backend
- Add request signing

---

## Mobile Considerations

✅ Works on Mobile:
- iOS Safari (may require user interaction)
- Android Chrome
- Android Firefox

⚠️ May need:
- Larger touch targets
- Full-screen mode option
- Permission prompts

❌ Limitations:
- iOS requires user gesture to request permissions
- Some browsers restrict camera access

---

## Troubleshooting

**Camera not starting:**
1. Check browser permissions
2. Try different browser
3. Reload page
4. Check console for errors

**Frames not being sent:**
1. Check backend URL in code (line 4)
2. Verify FastAPI is running
3. Check Network tab in DevTools
4. Look for 404 or 500 errors

**Backend not receiving frames:**
1. Check backend endpoint is correct
2. Verify request JSON format
3. Check backend logs
4. Test endpoint with Postman

**High CPU/Memory:**
1. Reduce video resolution (not recommended)
2. Increase capture interval (e.g., 3000ms)
3. Reduce JPEG quality (not recommended)
4. Check for memory leaks

---

## Next: Backend Integration

When implementing backend `/mark-attendance` endpoint:

```python
@app.post("/mark-attendance")
async def mark_attendance(request: dict):
    frame_base64 = request["frame"]  # Contains data:image/jpeg;base64,...
    timestamp = request["timestamp"]  # ISO format timestamp
    
    # 1. Decode base64 frame
    # 2. Run face recognition
    # 3. If recognized, mark attendance in DB
    # 4. Return response
    
    return {
        "status": "ok",
        "detected": True,
        "name": "Rohan",
        "message": "Attendance marked"
    }
```

---

## Questions?

Check:
1. IMPLEMENTATION_SUMMARY.md - Full overview
2. CAMERA_COMPONENT_DOCS.md - Detailed documentation
3. CameraAttendance.jsx - Source code with comments
4. Browser console - Debug logs
