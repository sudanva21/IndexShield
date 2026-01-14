import { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import { ShieldCheck, Menu, X } from 'lucide-react';

export default function Navbar() {
    const [isOpen, setIsOpen] = useState(false);
    const [scrolled, setScrolled] = useState(false);

    useEffect(() => {
        const handleScroll = () => setScrolled(window.scrollY > 20);
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    const navLinks = [
        { name: 'Home', path: '/' },
        { name: 'Scanner', path: '/scanner' },
        { name: 'Technology', path: '/technology' },
    ];

    return (
        <nav className={`navbar ${scrolled ? 'scrolled' : ''}`}>
            <div className="container nav-container">
                {/* Logo */}
                <NavLink to="/" className="nav-logo">
                    <ShieldCheck className="w-8 h-8 text-blue-500" size={32} color="var(--accent)" />
                    <span>Inbox<span style={{ color: 'var(--accent)' }}>Shield</span></span>
                </NavLink>

                {/* Desktop Menu */}
                <div className="nav-links">
                    {navLinks.map((link) => (
                        <NavLink
                            key={link.path}
                            to={link.path}
                            className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
                        >
                            {link.name}
                        </NavLink>
                    ))}
                    <NavLink
                        to="/scanner"
                        className="btn btn-primary"
                    >
                        Launch App
                    </NavLink>
                </div>

                {/* Mobile Toggle */}
                <button
                    className="mobile-toggle"
                    onClick={() => setIsOpen(!isOpen)}
                >
                    {isOpen ? <X size={24} /> : <Menu size={24} />}
                </button>
            </div>

            {/* Mobile Menu */}
            {isOpen && (
                <div className="mobile-menu">
                    {navLinks.map((link) => (
                        <NavLink
                            key={link.path}
                            to={link.path}
                            onClick={() => setIsOpen(false)}
                            className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
                        >
                            {link.name}
                        </NavLink>
                    ))}
                    <NavLink
                        to="/scanner"
                        onClick={() => setIsOpen(false)}
                        className="btn btn-primary"
                        style={{ width: '100%' }}
                    >
                        Launch App
                    </NavLink>
                </div>
            )}
        </nav>
    );
}
