import React from 'react'
import './App.css'
import { uploadFile } from './api'
function App() {
  const onFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) { uploadFile(event.target.files[0]) }

  }
  return (
    <>
      <input type="file" onChange={onFileChange} />
    </>
  )
}

export default App
