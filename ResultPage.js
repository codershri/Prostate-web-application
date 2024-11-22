import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useLocation } from 'react-router-dom';

const ResultPage = () => {
    const location = useLocation();
    const [result, setResult] = useState(null);

    useEffect(() => {
        const fetchResults = async () => {
            const imageId = new URLSearchParams(location.search).get('imageId');
            try {
                const response = await axios.get(`http://localhost:5000/results/${imageId}`);
                setResult(response.data);
            } catch (err) {
                console.error(err);
                alert('Error fetching results.');
            }
        };
        fetchResults();
    }, [location]);

    if (!result) return <div>Loading results...</div>;

    return (
        <div className="container">
            <h2>Analysis Results</h2>
            <img src={result.originalImage} alt="Uploaded MRI" style={{ width: '300px' }} />
            <h3>Classification: {result.label}</h3>
            <h4>Highlighted Cancer Region:</h4>
            <img src={result.cancerOverlay} alt="Highlighted Regions" style={{ width: '300px' }} />
        </div>
    );
};

export default ResultPage;
