import { Box, Heading, Button, Input, VStack, Text, useToast } from "@chakra-ui/react";
import { useRef, useState } from "react";

export default function Dashboard() {
  const [location, setLocation] = useState("");
  const [file, setFile] = useState(null);
  const [plan, setPlan] = useState(null);
  const toast = useToast();
  const fileInput = useRef();

  // Replace below with real API endpoint
  const API_URL = process.env.REACT_APP_API_URL || "https://your-backend.com";

  const handleUpload = async () => {
    if (!file || !location) {
      toast({ title: "Please enter location and upload inventory.", status: "warning" });
      return;
    }
    // Demo: Replace with real API call
    const payload = { location: location, inventory: "file-content" };
    setPlan({ translated: { orders: "Sample order" }, briefing: "AI-generated summary." });
    toast({ title: "Plan generated (demo)", status: "success" });
  };

  return (
    <Box mt={16} p={8} bg="white" borderRadius="xl" boxShadow="lg" maxW="900px" mx="auto">
      <Heading color="#0093d5" mb={4}>
        Dashboard
      </Heading>
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
          Upload Inventory File
        </Button>
        <input
          ref={fileInput}
          type="file"
          style={{ display: "none" }}
          onChange={(e) => setFile(e.target.files[0])}
        />
        <Button colorScheme="blue" onClick={handleUpload}>
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