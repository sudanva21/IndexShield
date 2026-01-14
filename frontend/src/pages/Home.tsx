import { Link } from 'react-router-dom';
import { ArrowRight, Shield, Zap, Lock } from 'lucide-react';
import Layout from '../components/Layout';

export default function Home() {
    return (
        <Layout>
            {/* Hero Section */}
            <section className="hero">
                <div className="container" style={{ position: 'relative', zIndex: 10 }}>

                    <div className="badge">
                        <span style={{ width: 8, height: 8, borderRadius: '50%', background: 'var(--accent)', display: 'block' }} />
                        v1.0 Now Live
                    </div>

                    <h1>
                        Secure Your Inbox with
                        <br />
                        <span style={{ color: 'var(--accent)' }}>AI-Powered Detection</span>
                    </h1>

                    <p>
                        Stop spam, phishing, and malicious emails before they reach your eyes.
                        InboxShield uses advanced machine learning to filter your messages with 99% accuracy.
                    </p>

                    <div className="hero-actions">
                        <Link
                            to="/scanner"
                            className="btn btn-primary"
                        >
                            Start Scanning
                            <ArrowRight size={18} />
                        </Link>
                        <Link
                            to="/technology"
                            className="btn btn-secondary"
                        >
                            How it works
                        </Link>
                    </div>
                </div>

                {/* Decorative Background Elements */}
                <div style={{
                    position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)',
                    width: '600px', height: '600px',
                    background: 'linear-gradient(to top right, var(--accent), #a855f7)',
                    opacity: 0.15, filter: 'blur(80px)', borderRadius: '50%', zIndex: 0
                }} />
            </section>

            {/* Features Grid */}
            <section className="features-section">
                <div className="container">
                    <div className="features-grid">
                        {[
                            {
                                icon: <Zap size={32} color="#eab308" />,
                                title: 'Real-time Analysis',
                                description: 'Get instant results. Our optimized engine processes text in milliseconds.'
                            },
                            {
                                icon: <Shield size={32} color="var(--accent)" />,
                                title: '99% Accuracy',
                                description: 'Trained on over 100,000 verified samples to minimize false positives.'
                            },
                            {
                                icon: <Lock size={32} color="var(--success)" />,
                                title: 'Privacy First',
                                description: 'We never store your personal emails. Analysis happens in volatile memory.'
                            }
                        ].map((feature, i) => (
                            <div key={i} className="feature-card">
                                <div className="feature-icon">
                                    {feature.icon}
                                </div>
                                <h3>{feature.title}</h3>
                                <p>{feature.description}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>
        </Layout>
    );
}
