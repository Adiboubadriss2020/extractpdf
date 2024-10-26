import React, { useState } from 'react';
import FileUpload from './components/FileUpload';

const App = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleUpload = async (file) => {
        setLoading(true);
        setError(null);

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('http://localhost:5000/extract-data', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            console.log(JSON.stringify(result, null, 2)); // Debug log to check structure
            setData(result.data);
        } catch (err) {
            setError(`Failed to extract data from the PDF: ${err.message}`);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ padding: '20px' }}>
            <h1>PDF Table Extractor</h1>
            <FileUpload onUpload={handleUpload} />
            {loading && <p>Loading...</p>}
            {error && <p style={{ color: 'red' }}>{error}</p>}
            {data && (
                <div>
                    <h2>Extracted Data</h2>
                    {data.length > 0 ? (
                        data.map((item, index) => (
                            <div key={index}>
                                <h3>Table {index + 1}</h3>
                                <table border="1" style={{ marginBottom: '20px', width: '100%', borderCollapse: 'collapse' }}>
                                    <thead>
                                        <tr>
                                            {item.headers.map((header, i) => (
                                                <th key={i} style={{ padding: '8px', backgroundColor: '#f2f2f2' }}>{header}</th>
                                            ))}
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {item.data.map((row, j) => (
                                            <tr key={j}>
                                                {row.map((cell, k) => (
                                                    <td key={k} style={{ padding: '8px' }}>{cell}</td>
                                                ))}
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        ))
                    ) : (
                        <p>No tables extracted from the PDF.</p>
                    )}
                </div>
            )}
        </div>
    );
};

export default App;
