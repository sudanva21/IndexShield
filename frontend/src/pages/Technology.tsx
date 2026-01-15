import { Share2, Fingerprint, Search } from 'lucide-react';
import Layout from '../components/Layout';

export default function Technology() {
    return (
        <Layout>
            <section style={{ padding: '5rem 0' }}>
                <div className="container" style={{ maxWidth: '800px' }}>
                    <div className="text-center" style={{ marginBottom: '4rem' }}>
                        <h1 style={{ fontSize: 'clamp(2rem, 5vw, 2.5rem)', fontWeight: 800, marginBottom: '1rem', color: 'var(--primary)' }}>Under the Hood</h1>
                        <p style={{ fontSize: 'clamp(1rem, 2vw, 1.25rem)', color: 'var(--text-muted)' }}>
                            How InboxShield distinguishes between valuable messages and digital noise.
                        </p>
                    </div>

                    <div style={{ position: 'relative' }}>
                        {/* Pipeline Steps */}
                        <div style={{ display: 'grid', gap: '3rem' }}>

                            <div className="tech-step">
                                <div className="step-number">1</div>
                                <div>
                                    <h3 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--primary)' }}>
                                        <Share2 size={24} /> Advanced Processing (N-Grams)
                                    </h3>
                                    <p style={{ color: 'var(--text-muted)', lineHeight: 1.6 }}>
                                        We analyze not just words, but <strong>phrases</strong> (N-grams). The model understands "not a winner" is different from "winner".
                                        We also calculate <strong>Spam Density</strong> and <strong>Sentiment Scores</strong> to detect hidden threats.
                                    </p>
                                </div>
                            </div>

                            <div className="tech-step">
                                <div className="step-number">2</div>
                                <div>
                                    <h3 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--primary)' }}>
                                        <Fingerprint size={24} /> Feature Fusion
                                    </h3>
                                    <p style={{ color: 'var(--text-muted)', lineHeight: 1.6 }}>
                                        Our <strong>Hybrid Pipeline</strong> combines text vectors with structural metadata (Caps Ratio, Punctuation Volume).
                                        It flags "screaming" messages (ALL CAPS) or "Keyword Stuffing" attacks that traditional models miss.
                                    </p>
                                </div>
                            </div>

                            <div className="tech-step">
                                <div className="step-number">3</div>
                                <div>
                                    <h3 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--primary)' }}>
                                        <Search size={24} /> SVM Classification
                                    </h3>
                                    <p style={{ color: 'var(--text-muted)', lineHeight: 1.6 }}>
                                        We use a <strong>Linear Support Vector Machine (SGD)</strong> optimized for high-dimensional data.
                                        It draws a hyper-precise decision boundary between complex Spam and Ham patterns.
                                    </p>
                                </div>
                            </div>

                        </div>
                    </div>
                </div>
            </section>
        </Layout>
    );
}
