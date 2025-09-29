import { ToastContainer } from "react-toastify";
import Footer from '../components/Footer';
import { Header } from '../components/Header';
import { Outlet } from 'react-router-dom';
import Section from '../components/Section';
export const MainLayout = () => {
  return (
    <>
      <div className="min-h-screen flex flex-col bg-neutral-100 text-shadow-gray-900">
       
      <Header/>
      <Section/>

        <main className="flex-1 px-4 py-6">
          <Outlet />
        </main>
        <Footer />
      </div>
       <ToastContainer position="top-right" autoClose={3000} />
    </>
  )
}
