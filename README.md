# Smart Attendance System

A real-time face recognition attendance tracking system combining computer vision with a modern web interface. Automatically detects and recognizes students' faces to mark attendance with zero manual intervention.

## Features

- **Real-time Face Detection**: Uses DNN (Deep Neural Networks) and Haar Cascade classifiers for accurate face detection
- **Face Recognition**: Advanced facial encoding and matching to identify registered students
- **Live Dashboard**: React-based web interface with real-time attendance tracking
- **Cloud Database**: Supabase integration for secure attendance records
- **Multi-Detection Methods**: Supports both DNN and Haar Cascade detection approaches
- **Automatic Duplicate Prevention**: Prevents marking the same student multiple times per day
- **Cross-platform**: Works on Windows, macOS, and Linux systems

## Project Structure

```
smart-attendance-system/
├── app/                           # Face detection utilities
│   ├── dnn_face_detector.py      # DNN-based face detection
│   ├── face_detector.py          # Haar Cascade detection
│   └── supabase_db.py            # Database operations
├── backend/                       # FastAPI server
│   ├── main.py                   # API endpoints
│   ├── attendance_service.py     # Attendance processing
│   └── face_recognition_service.py # Face encoding & matching
├── frontend-react/                # React + Vite web dashboard
│   ├── src/
│   │   ├── App.jsx               # Main application
│   │   └── components/
│   │       └── CameraAttendance.jsx # Live camera component
│   └── package.json
├── scripts/                       # Data preparation
│   ├── capture_faces.py          # Capture face samples
│   ├── generate_embeddings.py    # Generate face encodings
│   └── recognize_face.py         # Test recognition
├── data/
│   ├── faces/                    # Student face samples
│   └── attendance/               # Attendance logs
├── models/                        # Pre-trained detection models
│   ├── deploy.prototxt           # DNN configuration
│   └── res10_300x300_ssd_iter_140000.caffemodel # DNN weights
└── haarcascade_frontalface_default.xml # Haar Cascade model
```

## Tech Stack

**Frontend:**
- React 19.2
- Vite 7.2 (build tool)
- JavaScript/CSS

**Backend:**
- Python 3.x
- FastAPI (REST API)
- OpenCV (computer vision)
- face_recognition (facial encoding)
- Supabase (database)

**Machine Learning:**
- OpenCV DNN Module (face detection)
- face_recognition library (face encoding/matching)

## Prerequisites

Before getting started, ensure you have:

- Python 3.8+ installed
- Node.js 16+ installed
- A working webcam
- Supabase account (for database)
- Git for version control

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd smart-attendance-system
```

### 2. Set Up Python Backend

Create and activate a Python virtual environment:

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

Install Python dependencies:

```bash
pip install fastapi uvicorn opencv-python face-recognition supabase python-multipart
```

### 3. Configure Supabase

1. Create a Supabase project at [supabase.com](https://supabase.com)
2. Create a table named `attendance` with columns: `id`, `name`, `date`, `time`
3. Update Supabase credentials in:
   - [app/supabase_db.py](app/supabase_db.py)
   - [backend/attendance_service.py](backend/attendance_service.py)
   - [backend/main.py](backend/main.py)

### 4. Set Up Frontend

Navigate to the frontend directory and install dependencies:

```bash
cd frontend-react
npm install
```

## Quick Start

### Step 1: Capture Student Faces

Run the face capture script for each student:

```bash
python scripts/capture_faces.py
```

When prompted, enter the student's name. The script will capture 30 face images from your webcam. Press 'q' to stop early.

**Note:** Ensure good lighting and multiple angles for better recognition accuracy.

### Step 2: Start the Backend Server

```bash
python -m uvicorn backend.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

### Step 3: Start the Frontend Development Server

In a new terminal:

```bash
cd frontend-react
npm run dev
```

The web dashboard will be available at `http://localhost:5173`

### Step 4: Mark Attendance

1. Open the web dashboard in your browser
2. Click "Start Camera" to begin face detection
3. Position your face in front of the camera
4. The system will automatically recognize and mark your attendance
5. View attendance records in the dashboard

## API Endpoints

### Mark Attendance

**POST** `/mark-attendance`

Processes a video frame and marks attendance for recognized faces.

**Request:**
```json
{
  "frame": "data:image/jpeg;base64,/9j/4AAQSkZ...",
  "timestamp": "2024-02-02T10:30:00"
}
```

**Response:**
```json
{
  "success": true,
  "marked": ["john_doe", "jane_smith"]
}
```

### Get Attendance Records

**GET** `/attendance`

Retrieves all attendance records.

**Response:**
```json
[
  {
    "id": 1,
    "name": "john_doe",
    "date": "2024-02-02",
    "time": "10:30:45"
  }
]
```

## Development

### Running Tests

Test face detection with your webcam:

```bash
python main.py
```

This runs the DNN face detector in real-time. Press 'q' to exit.

### Testing Face Recognition

```bash
python scripts/recognize_face.py
```

### Code Quality

Lint the frontend code:

```bash
cd frontend-react
npm run lint
```

## Troubleshooting

### Camera Not Accessible
- Ensure no other application is using the camera
- Grant camera permissions in your OS settings
- Try a different USB port (for external cameras)

### Face Recognition Inaccurate
- Capture more face images for each student (30+ per person)
- Ensure diverse angles and lighting conditions
- Try adjusting the confidence threshold in [app/dnn_face_detector.py](app/dnn_face_detector.py)

### Backend Connection Errors
- Verify Supabase credentials are correct
- Check internet connectivity
- Ensure the FastAPI server is running on port 8000

### Frontend Not Loading Data
- Check browser console for errors (F12 → Console)
- Verify backend is running and accessible
- Clear browser cache and reload

## Performance Notes

- **Face Detection Speed**: ~30-50ms per frame (DNN method)
- **Recognition Accuracy**: ~95%+ with adequate training data
- **System Requirements**: 4GB RAM minimum, 2GB GPU optional

## Security Considerations

⚠️ **Important**: The Supabase credentials in this project are for development only.

For production deployment:
- Move credentials to environment variables (`.env` file)
- Use Supabase RLS (Row-Level Security) policies
- Implement proper authentication
- Add access controls to API endpoints
- Store face embeddings securely

## Future Enhancements

- [ ] User authentication and login system
- [ ] Multi-camera support
- [ ] Attendance analytics and reporting
- [ ] Email notifications
- [ ] Mobile app integration
- [ ] Advanced anti-spoofing detection
- [ ] Real-time performance metrics dashboard
- [ ] Batch attendance import/export

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

Please ensure code follows the existing style and includes documentation.

## License

This project is provided as-is for educational and organizational purposes. See [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or suggestions:

- Open an issue on GitHub
- Check existing documentation in [frontend-react/](frontend-react/) directory
- Review component documentation: [frontend-react/CAMERA_COMPONENT_DOCS.md](frontend-react/CAMERA_COMPONENT_DOCS.md)

## Maintainers

- **Project Lead**: Rohan
- **Frontend**: React/Vite team
- **Backend**: Python/FastAPI team
- **ML/Computer Vision**: Face recognition team

## Acknowledgments

- OpenCV for computer vision capabilities
- face_recognition library for facial encoding
- FastAPI for the REST framework
- React community for UI components
- Supabase for backend services

---

**Last Updated**: February 2024
