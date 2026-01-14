import { useState } from 'react';
import { AlertCircle, CheckCircle, Send, Loader2 } from 'lucide-react';
import Layout from '../components/Layout';

export default function Scanner() {
    const [text, setText] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<{ prediction: string; confidence: number } | null>(null);
    const [error, setError] = useState('');

    const handleScan = async () => {
        if (!text.trim()) return;

        setLoading(true);
        setError('');
        setResult(null);

        try {
            // Use environment variable for API URL in production, fallback to proxy in dev
            const baseUrl = import.meta.env.VITE_API_URL || '';
            const response = await fetch(`${baseUrl}/predict`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text }),
            });

            if (!response.ok) throw new Error('Failed to analyze text');

            const data = await response.json();
            setResult(data);
        } catch (err: any) {
            setError('Something went wrong. Please check your connection.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Layout>
            <section className="scanner-section">
                <div className="container" style={{ maxWidth: '800px' }}>
                    <div className="text-center mb-10">
                        <h1 style={{ fontSize: '2.5rem', fontWeight: 800, marginBottom: '1rem', color: 'var(--primary)' }}>Spam Scanner</h1>
                        <p style={{ color: 'var(--text-muted)' }}>
                            Paste your email or message content below to check for spam indicators.
                        </p>
                    </div>

                    <div className="scanner-box">
                        <textarea
                            className="scanner-input"
                            placeholder="Paste email content here..."
                            value={text}
                            onChange={(e) => setText(e.target.value)}
                        />

                        <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
                            <button
                                onClick={handleScan}
                                disabled={loading || !text.trim()}
                                className="btn btn-primary"
                                style={{ opacity: loading || !text.trim() ? 0.6 : 1, cursor: loading ? 'wait' : 'pointer' }}
                            >
                                {loading ? (
                                    <>
                                        <Loader2 size={18} className="animate-spin" style={{ animation: 'spin 1s linear infinite' }} />
                                        Analyzing...
                                    </>
                                ) : (
                                    <>
                                        <Send size={18} />
                                        Analyze Text
                                    </>
                                )}
                            </button>
                        </div>
                    </div>

                    {/* Results Section */}
                    {error && (
                        <div style={{ marginTop: '2rem', padding: '1rem', background: '#fef2f2', color: '#ef4444', borderRadius: 'var(--radius-md)', display: 'flex', alignItems: 'center', gap: '1rem', border: '1px solid #fecaca' }}>
                            <AlertCircle size={24} />
                            {error}
                        </div>
                    )}

                    {result && (
                        <div className={`result-box ${result.prediction === 'spam' ? 'is-spam' : 'is-ham'}`}>

                            {/* Result Badge */}
                            <div className="prediction-badge">
                                <div className="prediction-icon">
                                    {result.prediction === 'spam' ? <AlertCircle size={40} /> : <CheckCircle size={40} />}
                                </div>
                                <h2 style={{ fontSize: '1.5rem', fontWeight: 800, textTransform: 'uppercase', color: 'var(--primary)' }}>{result.prediction}</h2>
                            </div>

                            {/* Meter */}
                            <div style={{ flex: 1, width: '100%' }}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem', fontWeight: 600, color: 'var(--text-muted)' }}>
                                    <span>Confidence Score</span>
                                    <span>{result.confidence}%</span>
                                </div>
                                <div style={{ width: '100%', height: '12px', background: '#e2e8f0', borderRadius: '999px', overflow: 'hidden' }}>
                                    <div
                                        style={{
                                            width: `${result.confidence}%`,
                                            height: '100%',
                                            background: result.prediction === 'spam' ? 'var(--danger)' : 'var(--success)',
                                            transition: 'width 1s ease-out'
                                        }}
                                    />
                                </div>
                                <p style={{ marginTop: '1rem', color: 'var(--text-muted)', fontSize: '0.875rem' }}>
                                    {result.prediction === 'spam'
                                        ? 'This message shows strong patterns associated with spam, phishing, or unsolicited marketing.'
                                        : 'This message appears safe and does not exhibit common spam characteristics.'
                                    }
                                </p>
                            </div>

                        </div>
                    )}
                </div>
            </section>
        </Layout>
    );
}
