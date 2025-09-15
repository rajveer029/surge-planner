import { Box, Heading, Button, Input, VStack, Text } from "@chakra-ui/react";
import { useRef, useState } from "react";

export default function Dashboard() {
  const [location, setLocation] = useState("");
  const [file, setFile] = useState(null);
  const [plan, setPlan] = useState(null);
  const [loading, setLoading] = useState(false);
  const [alert, setAlert] = useState(null);
  const fileInput = useRef();

  const showAlert = (type, title, description) => {
    setAlert({ type, title, description });
    setTimeout(() => setAlert(null), 4000);
  };

  const getAlertColors = (type) => {
    switch (type) {
      case 'success':
        return { bg: '#C6F6D5', border: '#68D391', color: '#22543D' };
      case 'error':
        return { bg: '#FED7D7', border: '#FC8181', color: '#742A2A' };
      case 'warning':
        return { bg: '#FEFCBF', border: '#F6E05E', color: '#744210' };
      case 'info':
      default:
        return { bg: '#BEE3F8', border: '#63B3ED', color: '#2A4365' };
    }
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      showAlert("info", "File Selected", `${selectedFile.name} is ready for upload`);
    }
  };

  const handleUpload = async () => {
    if (!file || !location) {
      showAlert("warning", "Missing Information", "Please enter your hospital location and upload an inventory file before generating a plan.");
      return;
    }

    // Validate file type
    if (file && !file.name.match(/\.(csv|xlsx|xls|json)$/i)) {
      showAlert("error", "Invalid File Type", "Please upload a CSV, Excel, or JSON file.");
      return;
    }

    setLoading(true);
    setAlert(null);
    
    try {
      showAlert("info", "Generating Plan", "Processing your inventory data...");

      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      setPlan({ 
        translated: { orders: "Sample order based on current inventory levels" }, 
        briefing: "AI-generated surge plan summary based on your location and inventory data." 
      });
      
      showAlert("success", "Plan Generated Successfully", "Your surge plan is ready for review.");
    } catch (error) {
      showAlert("error", "Generation Failed", "There was an error generating your surge plan. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box mt={16} p={8} bg="white" borderRadius="xl" boxShadow="lg" maxW="900px" mx="auto">
      <Heading color="#0093d5" mb={4}>
        Dashboard
      </Heading>
      
      {alert && (
        <Box
          mb={4}
          p={4}
          borderRadius="md"
          border="1px solid"
          bg={getAlertColors(alert.type).bg}
          borderColor={getAlertColors(alert.type).border}
          color={getAlertColors(alert.type).color}
        >
          <Text fontWeight="bold" mb={1}>{alert.title}</Text>
          <Text fontSize="sm">{alert.description}</Text>
        </Box>
      )}
      
      <VStack spacing={4} align="stretch">
        <Input
          placeholder="Enter your hospital location (city or lat,lon)"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
        />
        <Button
          colorScheme="blue"
          variant="outline"
          onClick={() => fileInput.current.click()}
        >
          {file ? `Selected: ${file.name}` : "Upload Inventory File"}
        </Button>
        <input
          ref={fileInput}
          type="file"
          style={{ display: "none" }}
          accept=".csv,.xlsx,.xls,.json"
          onChange={handleFileChange}
        />
        <Button 
          colorScheme="blue" 
          onClick={handleUpload}
          isLoading={loading}
          loadingText="Generating Plan..."
        >
          Generate Surge Plan
        </Button>
      </VStack>
      {plan && (
        <Box mt={8} bg="#f2f2f2" p={5} borderRadius="md">
          <Heading size="md" color="#003399" mb={2}>
            Briefing
          </Heading>
          <Text color="#005b94">{plan.briefing}</Text>
          <Heading size="sm" color="#0093d5" mt={4}>
            Orders
          </Heading>
          <Text>{JSON.stringify(plan.translated.orders)}</Text>
        </Box>
      )}
    </Box>
  );
}
