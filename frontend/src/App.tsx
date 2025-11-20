import { useState, useEffect } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import './App.css'

// function App() {
//   const [count, setCount] = useState(0)

//   return (
//     <>
//       <div>
//         <a href="https://vite.dev" target="_blank">
//           <img src={viteLogo} className="logo" alt="Vite logo" />
//         </a>
//         <a href="https://react.dev" target="_blank">
//           <img src={reactLogo} className="logo react" alt="React logo" />
//         </a>
//       </div>
//       <h1>Vite + React</h1>
//       <div className="card">
//         <button onClick={() => setCount((count) => count + 1)}>
//           count is {count}
//         </button>
//         <p>
//           Edit <code>src/App.tsx</code> and save to test HMR
//         </p>
//       </div>
//       <p className="read-the-docs">
//         Click on the Vite and React logos to learn more
//       </p>
//     </>
//   )
// }

// export default App

function App() {
  const params = new URLSearchParams(window.location.search);
  const [jobBoard, setJobBoard] = useState([])

  const fetchCompanyJobBoard = async (companyName : string) => {
    const response = await fetch(`/api/data/${companyName}`)
    const result = await response.json();
    console.log(result);
    setJobBoard(result)
  }

  useEffect(() => {
    const company = params.get("company");
    // @ts-ignore
    fetchCompanyJobBoard(company)
  }, [])

  return (
    <>
      {jobBoard.map((job: any) => 
        <div>
          <h2>{job.title}</h2>
          <p>{job.jobDescription}</p>
        </div>
      )}
    </>
  )
}

export default App