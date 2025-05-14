import { useState } from 'react'
import './App.css'
import IntegerInput from "./IntegerInput.jsx";

function App() {
  const [image, setImage] = useState(null)
  const [randomizedImage, setRandomizedImage] = useState(null)
  const [loading, setLoading] = useState(false)
  const [tokenCount, setTokenCount] = useState(1)

  const handleImageUpload = (e) => {
    const file = e.target.files[0]
    if (file) {
      setImage(URL.createObjectURL(file))
    }
  }

  const handleRandomize = async () => {
    if (!image) return

    setLoading(true)
    const formData = new FormData()
    const response = await fetch(image)
    const blob = await response.blob()
    formData.append('image', blob)
    formData.append('randomTokenCount', tokenCount)

    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/randomize`, {
        method: 'POST',
        body: formData
      })
      const blob = await res.blob()
      setRandomizedImage(URL.createObjectURL(blob))
    } catch (error) {
      console.error('error randomizing image:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <h1>Token Randomizer</h1>
      <div className="upload-section">
        <input
          type="file"
          accept="image/*"
          onChange={handleImageUpload}
        />
        {image && (
          <button onClick={handleRandomize} disabled={loading}>
            {loading ? 'Randomizing...' : 'Randomize Token'}
          </button>
        )}
      </div>
      <IntegerInput onChange={setTokenCount} defaultValue={tokenCount}/>
      <div className="image-container">
        {image && !randomizedImage && (
          <div className="image-wrapper">
            <h2>Original Tokens</h2>
            <img src={image} alt="Original" />
          </div>
        )}
        {randomizedImage && (
          <div className="image-wrapper">
            <h2>Randomly Chosen Token(s)</h2>
            <img src={randomizedImage} alt="Randomized" />
          </div>
        )}
      </div>
    </div>
  )
}

export default App
