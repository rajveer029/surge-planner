import { Box, Heading, SimpleGrid, Text } from "@chakra-ui/react";
import { motion } from "framer-motion";

const services = [
  {
    title: "Location-based Planning",
    desc: "Get tailored surge plans based on your hospital’s location, local weather, and real-world context.",
  },
  {
    title: "Inventory Upload",
    desc: "Upload your current inventory (CSV/Excel) for precise stock and order recommendations.",
  },
  {
    title: "AI-Driven Insights",
    desc: "Benefit from GPT-powered event analysis and actionable, human-friendly briefings.",
  },
  {
    title: "Downloadable Reports",
    desc: "Receive downloadable, easy-to-read surge plans to share with your team.",
  },
];

export default function ServicesSection() {
  return (
    <motion.div
      id="services"
      initial={{ opacity: 0, y: 40 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 1.2 }}
      viewport={{ once: true }}
    >
      <Box p={8} maxW="1000px" mx="auto" mt={12}>
        <Heading textAlign="center" color="#0093d5" mb={8}>
          Services
        </Heading>
        <SimpleGrid columns={[1, 2]} spacing={8}>
          {services.map((svc, i) => (
            <Box
              key={i}
              bg="white"
              borderRadius="xl"
              boxShadow="md"
              p={6}
              borderLeft="6px solid #0093d5"
            >
              <Heading fontSize="xl" color="#003399" mb={2}>
                {svc.title}
              </Heading>
              <Text color="#005b94">{svc.desc}</Text>
            </Box>
          ))}
        </SimpleGrid>
      </Box>
    </motion.div>
  );
}