import { ShieldCheck } from 'lucide-react';

export default function Footer() {
    return (
        <footer style={{ background: 'white', borderTop: '1px solid var(--border)', padding: '4rem 0 2rem', marginTop: 'auto' }}>
            <div className="container">
                <div className="flex justify-between items-center" style={{ marginBottom: '2rem' }}>
                    <div className="flex items-center gap-2">
                        <ShieldCheck className="w-6 h-6 text-blue-500" size={24} color="var(--accent)" />
                        <span style={{ fontWeight: 'bold', fontSize: '1.25rem', color: 'var(--primary)' }}>InboxShield</span>
                    </div>
                    <div style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>
                        © {new Date().getFullYear()} InboxShield. All rights reserved.
                    </div>
                </div>
            </div>
        </footer>
    );
}
