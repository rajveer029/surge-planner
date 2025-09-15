import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalCloseButton,
  ModalBody,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  Button,
  Input,
  VStack,
  FormControl,
  FormErrorMessage,
  useToast,
} from "@chakra-ui/react";
import { useState } from "react";

export default function AuthModal({ isOpen, onClose, setLoggedIn }) {
  const [loading, setLoading] = useState(false);
  const toast = useToast();
  
  // Login form state
  const [loginData, setLoginData] = useState({
    email: "",
    password: ""
  });
  
  // Signup form state
  const [signupData, setSignupData] = useState({
    hospitalName: "",
    email: "",
    password: ""
  });
  
  // Form validation errors
  const [loginErrors, setLoginErrors] = useState({});
  const [signupErrors, setSignupErrors] = useState({});

  const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const validateLoginForm = () => {
    const errors = {};
    
    if (!loginData.email) {
      errors.email = "Email is required";
    } else if (!validateEmail(loginData.email)) {
      errors.email = "Please enter a valid email";
    }
    
    if (!loginData.password) {
      errors.password = "Password is required";
    } else if (loginData.password.length < 6) {
      errors.password = "Password must be at least 6 characters";
    }
    
    setLoginErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const validateSignupForm = () => {
    const errors = {};
    
    if (!signupData.hospitalName) {
      errors.hospitalName = "Hospital name is required";
    }
    
    if (!signupData.email) {
      errors.email = "Email is required";
    } else if (!validateEmail(signupData.email)) {
      errors.email = "Please enter a valid email";
    }
    
    if (!signupData.password) {
      errors.password = "Password is required";
    } else if (signupData.password.length < 6) {
      errors.password = "Password must be at least 6 characters";
    }
    
    setSignupErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const resetForms = () => {
    setLoginData({ email: "", password: "" });
    setSignupData({ hospitalName: "", email: "", password: "" });
    setLoginErrors({});
    setSignupErrors({});
  };

  const handleClose = () => {
    resetForms();
    onClose();
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    
    if (!validateLoginForm()) {
      toast({
        title: "Validation Error",
        description: "Please fix the errors below",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
      return;
    }
    
    setLoading(true);
    
    try {
      // Simulate API call
      await new Promise((resolve, reject) => {
        setTimeout(() => {
          // Simulate random success/failure for demo
          if (Math.random() > 0.3) {
            resolve();
          } else {
            reject(new Error("Invalid email or password"));
          }
        }, 1000);
      });
      
      toast({
        title: "Login Successful",
        description: "Welcome back!",
        status: "success",
        duration: 3000,
        isClosable: true,
      });
      
      setLoggedIn(true);
      handleClose();
    } catch (err) {
      toast({
        title: "Login Failed",
        description: err.message || "Please check your credentials and try again",
        status: "error",
        duration: 4000,
        isClosable: true,
      });
    } finally {
      setLoading(false);
    }
  };

  const handleSignup = async (e) => {
    e.preventDefault();
    
    if (!validateSignupForm()) {
      toast({
        title: "Validation Error",
        description: "Please fix the errors below",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
      return;
    }
    
    setLoading(true);
    
    try {
      // Simulate API call
      await new Promise((resolve, reject) => {
        setTimeout(() => {
          // Simulate random success/failure for demo
          if (Math.random() > 0.2) {
            resolve();
          } else {
            reject(new Error("Email already exists"));
          }
        }, 1200);
      });
      
      toast({
        title: "Account Created",
        description: "Welcome to Surge Planner!",
        status: "success",
        duration: 3000,
        isClosable: true,
      });
      
      setLoggedIn(true);
      handleClose();
    } catch (err) {
      toast({
        title: "Signup Failed",
        description: err.message || "Please try again with different details",
        status: "error",
        duration: 4000,
        isClosable: true,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={handleClose} isCentered>
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>Login / Signup</ModalHeader>
        <ModalCloseButton />
        <ModalBody pb={6}>
          <Tabs isFitted>
            <TabList mb="1em">
              <Tab>Login</Tab>
              <Tab>Sign Up</Tab>
            </TabList>
            <TabPanels>
              <TabPanel>
                <form onSubmit={handleLogin}>
                  <VStack spacing={4}>
                    <FormControl isInvalid={loginErrors.email}>
                      <Input 
                        placeholder="Email" 
                        type="email" 
                        value={loginData.email}
                        onChange={(e) => setLoginData({...loginData, email: e.target.value})}
                      />
                      <FormErrorMessage>{loginErrors.email}</FormErrorMessage>
                    </FormControl>
                    
                    <FormControl isInvalid={loginErrors.password}>
                      <Input 
                        placeholder="Password" 
                        type="password" 
                        value={loginData.password}
                        onChange={(e) => setLoginData({...loginData, password: e.target.value})}
                      />
                      <FormErrorMessage>{loginErrors.password}</FormErrorMessage>
                    </FormControl>
                    
                    <Button 
                      colorScheme="blue" 
                      isLoading={loading} 
                      type="submit" 
                      w="100%"
                      loadingText="Logging in..."
                    >
                      Login
                    </Button>
                  </VStack>
                </form>
              </TabPanel>
              <TabPanel>
                <form onSubmit={handleSignup}>
                  <VStack spacing={4}>
                    <FormControl isInvalid={signupErrors.hospitalName}>
                      <Input 
                        placeholder="Hospital Name" 
                        value={signupData.hospitalName}
                        onChange={(e) => setSignupData({...signupData, hospitalName: e.target.value})}
                      />
                      <FormErrorMessage>{signupErrors.hospitalName}</FormErrorMessage>
                    </FormControl>
                    
                    <FormControl isInvalid={signupErrors.email}>
                      <Input 
                        placeholder="Email" 
                        type="email" 
                        value={signupData.email}
                        onChange={(e) => setSignupData({...signupData, email: e.target.value})}
                      />
                      <FormErrorMessage>{signupErrors.email}</FormErrorMessage>
                    </FormControl>
                    
                    <FormControl isInvalid={signupErrors.password}>
                      <Input 
                        placeholder="Password" 
                        type="password" 
                        value={signupData.password}
                        onChange={(e) => setSignupData({...signupData, password: e.target.value})}
                      />
                      <FormErrorMessage>{signupErrors.password}</FormErrorMessage>
                    </FormControl>
                    
                    <Button 
                      colorScheme="blue" 
                      isLoading={loading} 
                      type="submit" 
                      w="100%"
                      loadingText="Creating account..."
                    >
                      Sign Up
                    </Button>
                  </VStack>
                </form>
              </TabPanel>
            </TabPanels>
          </Tabs>
        </ModalBody>
      </ModalContent>
    </Modal>
  );
}