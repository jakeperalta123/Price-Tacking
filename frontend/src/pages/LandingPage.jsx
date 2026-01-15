import React, { useState, useEffect } from 'react';
import { ChevronLeft, ChevronRight, User, Mail, Lock, LogOut, PlusCircle, Search } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import ProductManager from './ProductManager'; 

const LandingPage = () => {
    const navigate = useNavigate();
    const [currentIndex, setCurrentIndex] = useState(0);
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    
    const [activeModal, setActiveModal] = useState(null); 
    const [priceTab, setPriceTab] = useState('create'); 

    useEffect(() => {
        const token = localStorage.getItem('access_token');
        setIsLoggedIn(!!token);
    }, []);

    const slides = [
        { title: "Price Track Standard", sub: "Starting at $0/mo", img: "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1920&q=80" },
        { title: "Price Track Premium", sub: "Real-time updates", img: "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?auto=format&fit=crop&w=1920&q=80" },
        { title: "Price Track Enterprise", sub: "Scale with precision", img: "https://images.unsplash.com/photo-1469285994282-454ceb49e63c?auto=format&fit=crop&w=1920&q=80" }
    ];

    const nextSlide = () => setCurrentIndex((prev) => (prev === slides.length - 1 ? 0 : prev + 1));
    const prevSlide = () => setCurrentIndex((prev) => (prev === 0 ? slides.length - 1 : prev - 1));

    const handleLogout = () => {
        localStorage.removeItem('access_token');
        setIsLoggedIn(false);
        setIsMenuOpen(false);
        alert("Logged out successfully");
    };

    return (
        <div className="relative h-screen w-full overflow-hidden font-sans">
            <div
                className="absolute inset-0 transition-all duration-1000 ease-in-out bg-cover bg-center"
                style={{ backgroundImage: `url(${slides[currentIndex].img})` }}
            >
                <div className="absolute inset-0 bg-black/30"/>
            </div>

            <nav className="absolute top-0 w-full flex justify-between items-center px-8 py-6 z-50">
                <div className="text-white text-2xl font-black tracking-tighter cursor-pointer" onClick={() => navigate('/')}>
                    CREATED BY <span className="font-light">JAKE</span>
                </div>

                <div className="hidden md:flex items-center gap-1">
                    {isLoggedIn && (
                        <>
                            <button 
                                onClick={() => { setActiveModal('price'); setPriceTab('create'); }}
                                className="text-white text-[11px] font-black uppercase tracking-[0.2em] px-6 py-2 hover:bg-white/10 rounded-lg transition-all"
                            >
                                Create Price
                            </button>
                            <button 
                                onClick={() => { setActiveModal('price'); setPriceTab('check'); }}
                                className="text-white text-[11px] font-black uppercase tracking-[0.2em] px-6 py-2 hover:bg-white/10 rounded-lg transition-all"
                            >
                                Check Price
                            </button>
                        </>
                    )}
                </div>

                <div className="relative">
                    <button
                        onClick={() => setIsMenuOpen(!isMenuOpen)}
                        className="p-2 rounded-full hover:bg-white/20 transition-all text-white backdrop-blur-sm"
                    >
                        <User size={24}/>
                    </button>
                    {isMenuOpen && (
                        <div className="absolute right-0 mt-4 w-56 bg-white/95 backdrop-blur-md rounded-2xl shadow-2xl py-3 text-gray-800 animate-in fade-in zoom-in duration-200">
                            {!isLoggedIn ? (
                                <>
                                    <button onClick={() => navigate('/login')} className="w-full text-left px-6 py-2.5 hover:bg-gray-100 font-bold">Sign In</button>
                                    <button onClick={() => navigate('/register')} className="w-full text-left px-6 py-2.5 hover:bg-gray-100 font-medium text-gray-500">Create Account</button>
                                </>
                            ) : (
                                <>
                                    <div className="px-6 py-2 text-[10px] font-black text-gray-400 uppercase tracking-widest">Account Settings</div>
                                    <button onClick={() => navigate('/profile', { state: { targetTab: 'profile'}})} className="w-full text-left px-6 py-2.5 hover:bg-gray-100 flex items-center gap-2">
                                        <Mail size={16} /> Update Email
                                    </button>
                                    <button onClick={() => navigate('/profile', { state: { targetTab: 'password'}})} className="w-full text-left px-6 py-2.5 hover:bg-gray-100 flex items-center gap-2">
                                        <Lock size={16} /> Change Password
                                    </button>
                                    <div className="border-t border-gray-100 my-2" />
                                    <button onClick={handleLogout} className="w-full text-left px-6 py-2.5 hover:bg-red-50 text-red-500 flex items-center gap-2">
                                        <LogOut size={16} /> Sign Out
                                    </button>
                                </>
                            )}
                        </div>
                    )}
                </div>
            </nav>

            {activeModal === 'price' && (
                <div className="absolute inset-0 z-[100] flex items-center justify-center bg-black/40 backdrop-blur-md animate-in fade-in duration-300">
                    <div className="absolute inset-0" onClick={() => setActiveModal(null)}/>
                    <ProductManager 
                        initialTab={priceTab} 
                        onClose={() => setActiveModal(null)} 
                    />
                </div>
            )}

            <div className="relative h-full flex flex-col items-center justify-start pt-32 text-white z-10 text-center pointer-events-none">
                <h1 className="text-5xl font-bold mb-2 animate-in fade-in slide-in-from-top-4 duration-700">
                    {slides[currentIndex].title}
                </h1>
                <p className="text-lg font-medium animate-in fade-in slide-in-from-top-6 duration-1000">
                    {slides[currentIndex].sub}
                </p>    
            </div>

            <button onClick={prevSlide} className="absolute left-6 top-1/2 -translate-y-1/2 p-2 text-white/50 hover:text-white transition-all z-20">
                <ChevronLeft size={48} />
            </button>
            <button onClick={nextSlide} className="absolute right-6 top-1/2 -translate-y-1/2 p-2 text-white/50 hover:text-white transition-all z-20">
                <ChevronRight size={48} />
            </button>

            <div className="absolute bottom-10 left-1/2 -translate-x-1/2 flex gap-3">
                {slides.map((_, i) => (
                    <div 
                        key={i} 
                        className={`h-1 rounded-full transition-all duration-500 ${currentIndex === i ? 'w-8 bg-white' : 'w-4 bg-white/40'}`} 
                    />
                ))}
            </div>
        </div>
    );
};

export default LandingPage;