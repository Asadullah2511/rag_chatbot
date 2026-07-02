import { useState, useRef, useEffect } from 'react'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function Message({ role, content }) {
  const isUser = role === 'user'
  return (
    <div style={{
      display: 'flex',
      justifyContent: isUser ? 'flex-end' : 'flex-start',
      marginBottom: '16px',
    }}>
      <div style={{
        maxWidth: '75%',
        padding: '14px 18px',
        borderRadius: isUser ? '18px 18px 4px 18px' : '18px 18px 18px 4px',
        background: isUser ? 'var(--user-msg)' : 'var(--bot-msg)',
        border: '1px solid var(--border)',
        color: 'var(--text-primary)',
        fontSize: '0.95rem',
        lineHeight: '1.65',
        whiteSpace: 'pre-wrap',
        wordBreak: 'break-word',
      }}>
        {content}
      </div>
    </div>
  )
}

function ThinkingDots() {
  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      gap: '4px',
      padding: '16px 20px',
      background: 'var(--bot-msg)',
      border: '1px solid var(--border)',
      borderRadius: '18px 18px 18px 4px',
      maxWidth: '100px',
    }}>
      {[0, 1, 2].map(i => (
        <span key={i} style={{
          width: '8px',
          height: '8px',
          borderRadius: '50%',
          background: 'var(--accent)',
          display: 'inline-block',
          animation: 'bounce 1.4s infinite ease-in-out',
          animationDelay: `${i * 0.16}s`,
        }} />
      ))}
    </div>
  )
}

export default function App() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: "Welcome to DR Psychology. I'm your research assistant for the paper *\"Trauma and Dark Psychology: Therapeutic Approaches to Manipulation, Control, and Power Abuse\"*. Ask me anything about dark psychology, trauma, or the therapeutic approaches discussed in the research.",
    },
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  async function handleSubmit(e) {
    e.preventDefault()
    const question = input.trim()
    if (!question || loading) return

    setInput('')
    setError(null)
    setMessages(prev => [...prev, { role: 'user', content: question }])
    setLoading(true)

    try {
      const res = await fetch(`${API_URL}/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
      })

      if (!res.ok) {
        const errText = await res.text()
        throw new Error(errText || `Server error: ${res.status}`)
      }

      const data = await res.json()
      setMessages(prev => [...prev, { role: 'assistant', content: data.answer }])
    } catch (err) {
      setError(err.message || 'Failed to get response. Is the backend running?')
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `Sorry, I couldn't reach the server. Make sure the backend is running on ${API_URL}. Error: ${err.message}`,
      }])
    } finally {
      setLoading(false)
    }
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      height: '100vh',
      maxWidth: 'var(--max-width)',
      margin: '0 auto',
      width: '100%',
      padding: '0 16px',
    }}>
      <header style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '16px 0',
        borderBottom: '1px solid var(--border)',
        flexShrink: 0,
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{
            width: '40px',
            height: '40px',
            borderRadius: '10px',
            background: 'linear-gradient(135deg, var(--accent), #a78bfa)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '18px',
            fontWeight: 700,
            color: '#fff',
            boxShadow: '0 0 20px var(--accent-glow)',
          }}>
            DR
          </div>
          <div>
            <h1 style={{
              fontSize: '1.2rem',
              fontWeight: 700,
              letterSpacing: '-0.02em',
              background: 'linear-gradient(135deg, var(--accent), #a78bfa)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
            }}>
              DR Psychology
            </h1>
            <p style={{
              fontSize: '0.75rem',
              color: 'var(--text-secondary)',
              marginTop: '-2px',
            }}>
              Research RAG Assistant
            </p>
          </div>
        </div>
        <a
          href="https://github.com/anomalyco/opencode"
          target="_blank"
          rel="noopener noreferrer"
          style={{
            color: 'var(--text-secondary)',
            fontSize: '0.8rem',
            textDecoration: 'none',
            transition: 'color 0.2s',
          }}
        >
          GitHub
        </a>
      </header>

      <main style={{
        flex: 1,
        overflowY: 'auto',
        padding: '24px 0',
      }}>
        {messages.map((msg, i) => (
          <Message key={i} role={msg.role} content={msg.content} />
        ))}
        {loading && (
          <div style={{
            display: 'flex',
            justifyContent: 'flex-start',
            marginBottom: '16px',
          }}>
            <ThinkingDots />
          </div>
        )}
        {error && (
          <div style={{
            padding: '10px 14px',
            background: 'rgba(248, 113, 113, 0.1)',
            border: '1px solid rgba(248, 113, 113, 0.3)',
            borderRadius: 'var(--radius)',
            color: 'var(--error)',
            fontSize: '0.85rem',
            marginBottom: '16px',
          }}>
            Connection error: {error}
          </div>
        )}
        <div ref={bottomRef} />
      </main>

      <footer style={{
        padding: '12px 0 20px',
        flexShrink: 0,
      }}>
        <form onSubmit={handleSubmit} style={{
          display: 'flex',
          gap: '8px',
          background: 'var(--bg-secondary)',
          border: '1px solid var(--border)',
          borderRadius: 'var(--radius-lg)',
          padding: '6px',
          transition: 'border-color 0.2s, box-shadow 0.2s',
        }}
          onFocusCapture={e => {
            e.currentTarget.style.borderColor = 'var(--accent)'
            e.currentTarget.style.boxShadow = '0 0 0 3px var(--accent-glow)'
          }}
          onBlurCapture={e => {
            e.currentTarget.style.borderColor = 'var(--border)'
            e.currentTarget.style.boxShadow = 'none'
          }}
        >
          <input
            type="text"
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask about dark psychology, trauma, or therapy..."
            disabled={loading}
            style={{
              flex: 1,
              background: 'transparent',
              border: 'none',
              outline: 'none',
              color: 'var(--text-primary)',
              fontSize: '0.95rem',
              padding: '10px 14px',
              fontFamily: 'inherit',
            }}
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            style={{
              background: 'linear-gradient(135deg, var(--accent), #a78bfa)',
              border: 'none',
              borderRadius: '10px',
              color: '#fff',
              cursor: loading || !input.trim() ? 'not-allowed' : 'pointer',
              opacity: loading || !input.trim() ? 0.5 : 1,
              padding: '10px 20px',
              fontSize: '0.9rem',
              fontWeight: 600,
              fontFamily: 'inherit',
              transition: 'opacity 0.2s, transform 0.1s',
              whiteSpace: 'nowrap',
            }}
          >
            {loading ? 'Thinking...' : 'Ask'}
          </button>
        </form>
        <p style={{
          textAlign: 'center',
          color: 'var(--text-secondary)',
          fontSize: '0.7rem',
          marginTop: '10px',
        }}>
          Powered by Groq LLM &middot; Answers based on research by Benjamin Pelz (2025)
        </p>
      </footer>

      <style>{`
        @keyframes bounce {
          0%, 80%, 100% { transform: translateY(0); }
          40% { transform: translateY(-8px); }
        }
        input::placeholder { color: var(--text-secondary); }
        button:active:not(:disabled) { transform: scale(0.97); }
        @media (max-width: 480px) {
          header { padding: 12px 0; }
          main { padding: 16px 0; }
          footer { padding: 8px 0 16px; }
          message div { max-width: 85%; font-size: 0.9rem; }
        }
      `}</style>
    </div>
  )
}
