import { Box, Heading, SimpleGrid, Text } from "@chakra-ui/react";
import { motion } from "framer-motion";

const benefits = [
  {
    title: "Public Safety",
    desc: "Improved surge readiness helps hospitals save more lives during crises and outbreaks.",
  },
  {
    title: "Resource Optimization",
    desc: "Reduce shortages and wastage by aligning supply orders with real, local needs.",
  },
  {
    title: "Transparency",
    desc: "Clear, easy-to-understand plans for staff and the public build community trust.",
  },
  {
    title: "Rapid Response",
    desc: "Faster, data-driven decision making in emergencies.",
  },
];

export default function BenefitsSection() {
  return (
    <motion.div
      id="benefits"
      initial={{ opacity: 0, y: 40 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 1.2 }}
      viewport={{ once: true }}
    >
      <Box p={8} maxW="1000px" mx="auto" mt={12}>
        <Heading textAlign="center" color="#0093d5" mb={8}>
          Benefits to the Public
        </Heading>
        <SimpleGrid columns={[1, 2]} spacing={8}>
          {benefits.map((b, i) => (
            <Box
              key={i}
              bg="white"
              borderRadius="xl"
              boxShadow="md"
              p={6}
              borderLeft="6px solid #005b94"
            >
              <Heading fontSize="xl" color="#003399" mb={2}>
                {b.title}
              </Heading>
              <Text color="#005b94">{b.desc}</Text>
            </Box>
          ))}
        </SimpleGrid>
      </Box>
    </motion.div>
  );
}