import { ChakraProvider, Box } from "@chakra-ui/react";
import Navbar from "./components/Navbar";
import HeroSection from "./components/HeroSection";
import AboutSection from "./components/AboutSection";
import ServicesSection from "./components/ServicesSection";
import BenefitsSection from "./components/BenefitsSection";
import AuthModal from "./components/AuthModal";
import Dashboard from "./components/Dashboard";
import Footer from "./components/Footer";
import { useState } from "react";

function App() {
  const [authOpen, setAuthOpen] = useState(false);
  const [loggedIn, setLoggedIn] = useState(false);

  return (
    <ChakraProvider>
      <Box bg="#e6f4fa" minH="100vh">
        <Navbar onAuthOpen={() => setAuthOpen(true)} loggedIn={loggedIn} setLoggedIn={setLoggedIn} />
        <HeroSection onAuthOpen={() => setAuthOpen(true)} />
        <AboutSection />
        <ServicesSection />
        <BenefitsSection />
        {authOpen && (
          <AuthModal
            isOpen={authOpen}
            onClose={() => setAuthOpen(false)}
            setLoggedIn={setLoggedIn}
          />
        )}
        {loggedIn && <Dashboard />}
        <Footer />
      </Box>
    </ChakraProvider>
  );
}
export default App;