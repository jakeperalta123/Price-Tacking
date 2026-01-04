import React, { useState, useEffect } from "react";
import { User, Mail, Lock, KeyRound, LogOut, Loader2, ShieldCheck, Home } from 'lucide-react';
import { authApi } from "../api/axios"; 
import InputField from "../components/InputField";
import { useNavigate, useLocation } from "react-router-dom";

function Profile() {
    const navigate = useNavigate();
    const location = useLocation();
    
    
    const [activeTab, setActiveTab] = useState(location.state?.targetTab || 'profile');
    const [isLoading, setIsLoading] = useState(true);

    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [currentPassword, setCurrentPassword] = useState('');
    const [newPassword, setNewPassword] = useState('');

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const response = await authApi.get('/users/me');
                setUsername(response.data.username);
                setEmail(response.data.email);
            } catch (error) {
                console.error("Unable to fetch data", error);
                if (error.response?.status === 401) {
                    localStorage.removeItem('access_token');
                    navigate('/login');
                }
            } finally {
                setIsLoading(false);
            }
        };
        fetchUserData();
    }, [navigate]);

    const handleUpdateUser = async (e) => {
        e.preventDefault();
        try {
            await authApi.patch('/users/update', { email: email });
            alert("Successfully updated Email");
        } catch (error) {
            alert("Update failed: " + (error.response?.data?.detail || "Internal server Error"));
        }
    };

    const handleUpdatePassword = async (e) => {
        e.preventDefault();
        try {
            await authApi.patch('/users/password', {
                current_password: currentPassword, 
                new_password: newPassword
            });
            alert("Successfully updated Password");
            setCurrentPassword('');
            setNewPassword('');
        } catch (error) {
            alert("Password update failed: " + (error.response?.data?.detail || "Error in current password"));
        }
    };

    const handleLogout = () => {
        localStorage.removeItem('access_token');
        navigate('/login');
    };

    if (isLoading) {
        return (
            <div className="flex justify-center items-center min-h-screen bg-[#111]">
                <Loader2 className="animate-spin text-white" size={48} />
            </div>
        );
    }

    return (
        <div className="relative min-h-screen w-full flex items-center justify-center font-sans overflow-hidden">
            <div 
                className="absolute inset-0 bg-cover bg-center z-0"
                style={{ backgroundImage: `url('https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1920&q=80')` }}
            >
                <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" />
            </div>

            
            <div className="relative z-10 w-full max-w-lg px-6 py-12">
                
                
                <div className="flex justify-between items-center mb-8">
                    <button
                        onClick={() => navigate('/')}
                        className="flex items-center gap-2 text-white/80 hover:text-white transition-all font-medium bg-white/10 px-5 py-2 rounded-full backdrop-blur-md border border-white/10 active:scale-95"
                    >
                        <Home size={18}/> Home
                    </button>
                    <button 
                        onClick={handleLogout} 
                        className="flex items-center gap-2 text-white/50 hover:text-red-400 transition-all text-sm px-4 py-2"
                    >
                        <LogOut size={16}/> Sign Out
                    </button>
                </div>

                <div className="bg-white/95 backdrop-blur-2xl rounded-[32px] shadow-2xl overflow-hidden border border-white/20 p-8 sm:p-10">
                    
                    <div className="mb-8 text-center sm:text-left">
                        <h1 className="text-3xl font-black text-gray-900 tracking-tight">
                            {activeTab === 'profile' ? 'Account Settings' : 'Security Settings'}
                        </h1>
                        <p className="text-gray-500 font-medium mt-1">
                            {activeTab === 'profile' ? 'Manage your contact information' : 'Protect your account'}
                        </p>
                    </div>

                    
                    <div className="flex p-1.5 bg-gray-100 rounded-2xl mb-8 border border-gray-200/50">
                        <button
                            onClick={() => setActiveTab('profile')}
                            className={`flex-1 py-3 text-sm font-bold rounded-xl flex justify-center items-center gap-2 transition-all
                            ${activeTab === 'profile' ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-400 hover:text-gray-600'}`}
                        >
                            <User size={18}/> Profile
                        </button>
                        <button
                            onClick={() => setActiveTab('password')}
                            className={`flex-1 py-3 text-sm font-bold rounded-xl flex justify-center items-center gap-2 transition-all
                            ${activeTab === 'password' ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-400 hover:text-gray-600'}`}
                        >
                            <ShieldCheck size={18}/> Security
                        </button>
                    </div>

                    
                    <div className="min-h-[300px]">
                        {activeTab === 'profile' ? (
                            <form onSubmit={handleUpdateUser} className="space-y-6 animate-in fade-in zoom-in-95 duration-500">
                                <div className="bg-gray-50 p-4 rounded-2xl border border-gray-100">
                                    <label className="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Account name</label>
                                    <div className="flex items-center gap-3 mt-1 px-1 text-gray-900 font-bold">
                                        <User size={18} className="text-gray-300"/>
                                        <span>{username}</span>
                                    </div>
                                </div>
                                <InputField
                                    label="Update Email"
                                    icon={Mail}
                                    placeholder="Enter new email"
                                    type="email"
                                    value={email}
                                    onChange={setEmail}
                                />
                                <div className="flex justify-center pt-6">
                                    <button 
                                        type="submit" 
                                        className="w-full max-w-[280px] bg-[#393c41] text-white py-4 rounded-full font-bold text-xs uppercase tracking-[0.15em] hover:bg-black transition-all active:scale-95 shadow-xl shadow-gray-200"
                                    >
                                        Save Changes
                                    </button>
                                </div>
                            </form>
                        ) : (
                            <form onSubmit={handleUpdatePassword} className="space-y-6 animate-in fade-in zoom-in-95 duration-500">
                                <InputField
                                    label="Current Password"
                                    icon={Lock}
                                    type="password"
                                    placeholder="Enter current password"
                                    value={currentPassword}
                                    onChange={setCurrentPassword}
                                />
                                <InputField
                                    label="New Password"
                                    icon={KeyRound}
                                    type="password"
                                    placeholder="Enter new password"
                                    value={newPassword}
                                    onChange={setNewPassword}
                                />
                                <div className="flex justify-center pt-6">
                                    <button 
                                        type="submit" 
                                        className="w-full max-w-[280px] bg-[#393c41] text-white py-4 rounded-full font-bold text-xs uppercase tracking-[0.15em] hover:bg-black transition-all active:scale-95 shadow-xl shadow-gray-200"
                                    >
                                        Update Password
                                    </button>
                                </div>
                            </form>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Profile;