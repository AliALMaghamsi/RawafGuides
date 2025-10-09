import { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";
import { AuthContext } from "../context/AuthContext";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error,setError]  = useState("");
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await api.post("/api/auth/login", { username, password });

      const token = res.data.access_token;
      login(token);

      const decoded = JSON.parse(atob(token.split(".")[1]));
      const userRole = decoded.role;
      const hotelsRes = await api.get("/api/guide/hotels/");
      console.log(hotelsRes.data);

      if (userRole === "admin") navigate("/admin-dashboard");
      else if (userRole === "guide") navigate("/guide-dashboard");
      else navigate("/");

    } catch (err) {
      setError("Invalid username or password");
    }
  };

  return (

        <div className="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-sm">
            
            <h2 className="mt-10 text-center text-2xl/9 font-bold tracking-tight text-gray-900">Sign in to your account</h2>
        </div>

        <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
            <form onSubmit={handleSubmit} className="space-y-6">
            <div>
                <label htmlFor="username" className="block text-sm/6 font-medium text-gray-900">Username</label>
                <div className="mt-2">
                <input value = {username} onChange = {e => setUsername(e.target.value)}id="username" type="username" name="username" required autoComplete="username" className="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6" />
                </div>
            </div>

            <div>
                <div className="flex items-center justify-between">
                <label htmlFor="password" className="block text-sm/6 font-medium text-gray-900">Password</label>
                
                </div>
                <div className="mt-2">
                <input value = {password} onChange={e => setPassword(e.target.value)} id="password" type="password" name="password" required autocomplete="current-password" className="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6" />
                </div>
            </div>

            <div>
                <button type="submit" className="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm/6 font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Sign in</button>
                {error && <p className='text-red-600 flex justify-center pt-2'>{error}</p>}
            </div>
            
            </form>

        </div>
        </div>

    
  )
}
