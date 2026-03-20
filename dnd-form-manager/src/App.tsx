import { useStore } from './store/useStore'
import './App.css'

function App() {
  const count = useStore((state) => state.count)
  const increment = useStore((state) => state.increment)
  const decrement = useStore((state) => state.decrement)
  const reset = useStore((state) => state.reset)

  return (
    <div className="card">
      <h1>Zustand + TS + Vite</h1>
      <h2>Count: {count}</h2>

      <div style={{ display: 'flex', gap: '10px', justifyContent: 'center' }}>
        <button onClick={decrement}>- Decrement</button>
        <button onClick={increment}>+ Increment</button>
        <button onClick={reset}>Reset</button>
      </div>
    </div>
  )
}

export default App
