import React, { useState } from "react"

function App() {
  const [files, setFiles] = useState([])

  const upload = async () => {
    const formData = new FormData()
    for (let f of files) {
      formData.append("files", f)
    }
    const res = await fetch("http://localhost:8989/upload", {
      method: "POST",
      body: formData,
    })
    const blob = await res.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = "result.zip"
    a.click()
  }

  return (
    <div style={{ textAlign: "center", marginTop: "80px" }}>
      <h2>圖片去外框 + 亮綠背景</h2>
      <input
        type="file"
        multiple
        onChange={(e) => setFiles(e.target.files)}
      />
      <br />
      <br />
      <button onClick={upload}>處理圖片</button>
    </div>
  )
}

export default App
