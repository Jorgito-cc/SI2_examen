
import AuthProvider from './context/AuthContex';
import MainRouter from './router/MainRoter'
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
export const App = () => {
  return (
    <>
 <AuthProvider>
      <MainRouter />
      <ToastContainer position="top-right" autoClose={3000} pauseOnHover />
    </AuthProvider>
    </>
  )
}
