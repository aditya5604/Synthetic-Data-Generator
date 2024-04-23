import { useState } from 'react'
import './App.css'
import axios from 'axios'

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [base64String, setBase64String] = useState('');
  const [resultImages, setResultImages] = useState([]);
  const [prompt , setPrompt] = useState('beautify the image');
  const [strength, setStrength] = useState(0);
  const [guidance, setGuidance] = useState('');
  const [negativePrompt, setNegativePrompt] = useState('');
  const [outputImageName, setOutputImageName] = useState('output.png');

  const handlePromptChange = (event) => {
    setPrompt(event.target.value);
  };
  
  const handleNegativePromptChange = (event) => {
    setNegativePrompt(event.target.value);
  };
  
  const handleStrengthChange = (event) => {
    setStrength(event.target.value);
  };
  
  const handleGuidanceChange = (event) => {
    setGuidance(event.target.value);
  };

  const handleOutputImageNameChange = (event) => {
    setOutputImageName(event.target.value);
  };
  
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
    if (file) {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onloadend = () => {
        setBase64String(reader.result);
      };
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/generate', { base64String, prompt, negativePrompt, strength, guidance , outputImageName });
      setResultImages(response.data.images);
    } catch (error) {
      console.error('Error fetching images:', error);
    }
  };

  return (
    <>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <input type="text" value={prompt} onChange={handlePromptChange} placeholder="Prompt" />
        <input type="text" value={negativePrompt} onChange={handleNegativePromptChange} placeholder="Negative Prompt (Optional)" />
        <input type="range" value={strength} onChange={handleStrengthChange} min="0" max="1" step="0.01" />
        <label>{strength}</label>
        <input type="range" value={guidance} onChange={handleGuidanceChange} min="0" max="1" step="0.01" />
        <label>{guidance}</label>
        <input type="text" value={outputImageName} onChange={handleOutputImageNameChange} placeholder="Output Image Name" />
        <button type="submit">Submit</button>
      </form>
      <div>
        {resultImages.map((image, index) => (
          <img key={index} src={`data:image/png;base64,${image}`} alt={`Image ${index}`} />
        ))}
      </div>
    </>
  )
}
export default App
