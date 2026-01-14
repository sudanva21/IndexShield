import type { ReactNode } from 'react';
import Navbar from './Navbar';
import Footer from './Footer';

interface LayoutProps {
    children: ReactNode;
    className?: string; // Allow custom classes just in case
}

export default function Layout({ children, className = "" }: LayoutProps) {
    return (
        <div className="flex-col" style={{ minHeight: '100vh', backgroundColor: 'var(--bg-light)' }}>
            <Navbar />
            <main style={{ flexGrow: 1, paddingBottom: '2rem' }} className={className}>
                {children}
            </main>
            <Footer />
        </div>
    );
}
