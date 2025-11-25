import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Layout from './components/Layout/Layout';
import A1Form from './components/Forms/A1Form';
import GHMForm from './components/Forms/GHMForm';
import KEMForm from './components/Forms/KEMForm';
import './App.css';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<A1Form />} />
          <Route path="/a1" element={<A1Form />} />
          <Route path="/ghm" element={<GHMForm />} />
          <Route path="/kem" element={<KEMForm />} />
        </Routes>
      </Layout>
      <ToastContainer
        position="top-right"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
      />
    </Router>
  );
}

export default App;



