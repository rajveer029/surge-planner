import { Box, Heading, Text } from "@chakra-ui/react";
import { motion } from "framer-motion";

export default function AboutSection() {
  return (
    <motion.div
      id="about"
      initial={{ opacity: 0, y: 40 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 1 }}
      viewport={{ once: true }}
    >
      <Box p={8} bg="white" maxW="900px" mx="auto" borderRadius="xl" boxShadow="lg" mt={12}>
        <Heading color="#0093d5" mb={4}>
          About Surge Planner
        </Heading>
        <Text color="#003399" fontSize="lg">
          Surge Planner is a WHO-inspired digital solution helping hospitals and healthcare
          organizations prepare for patient surges by combining inventory, location, and real-time
          weather data into actionable plans powered by advanced AI.
        </Text>
      </Box>
    </motion.div>
  );
}