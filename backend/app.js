const express = require('express');
const multer = require('multer');
const cors = require('cors');
const { PythonShell } = require('python-shell');
const path = require('path');
const app = express();
const upload = multer({ dest: 'uploads/' });

app.use(cors()); // Enable CORS for cross-origin requests

// Endpoint for file upload
app.post('/upload', upload.single('file'), (req, res) => {
    const filePath = path.join(__dirname, 'uploads', req.file.filename);

    PythonShell.run(
        path.join(__dirname, 'python/process_pdf.py'),
        { args: [filePath] },
        (err, result) => {
            if (err) return res.status(500).json({ error: err.message });
            res.json(JSON.parse(result[0])); // Expecting JSON string output from Python
        }
    );
});

app.listen(5000, () => {
    console.log('Server running on http://localhost:5000');
});
