import React, {useState} from "react";
import {Eye, EyeOff, Lock, Mail} from "lucide-react";
import axios from 'axios';
import {useNavigate} from 'react-router-dom';

function Login(){

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);
        
        try{
            const response = await axios.post('http://127.0.0.1:8000/auth/token', formData, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            });

            const {access_token} = response.data;

            localStorage.setItem('access_token', access_token);
            console.log("Successfully Logged In, Stored Token");
            alert("You son of a bitch, you logged in!");
            navigate('/');
        } catch(error){
            console.error("Log in failed", error.response?.data);
            alert("Log in failed" + (error.response?.data?.detail || "wrong username or password"))
        }
    }

    return (
        <div className="flex justify-center items-center min-h-screen bg-gray-100">
            <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
                <h2 className="text-2xl font-bold mb-6 text-center text-gray-800"> Login</h2>
                <form onSubmit={handleLogin} className="space-y-4">
                    <div className="relative">
                        <Mail className="absolute left-3 top-3 text-gray-400" size={20} />
                        <input 
                            type="email"
                            placeholder="Email"
                            className="w-full pl-10 pr-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>
                    <div className="relative">
                        <Lock className="absolute left-3 top-3 text-gray-400" size={20} />
                        <input 
                            type={showPassword ? "text" : "password"}
                            placeholder="Password"
                            className="w-full pl-10 pr-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                        <button
                            type="button"
                            onClick={() => setShowPassword(!showPassword)}
                            className="absolute right-3 top-3 text-gray-400 hover:text-gray-600"
                        >
                            {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                        </button>
                    </div>
                    <button
                        type="submit"
                        className="w-full bg-blue-600 text-white py-2 rounded-md font-semibold hover:bg-blue-700 transition duration-200"
                    >
                        Sign In
                    </button>
                </form>
                <p className="mt-4 text-center text-gray-600 text-sm">
                    Don't have an account?
                    <button onClick={() => navigate('/register')} className="text-blue-500 ml-1 hover:underline">
                        Register
                    </button>
                </p>
            </div>
        </div>
    )
}

export default Login