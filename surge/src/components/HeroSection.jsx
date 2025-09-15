import { Box, Heading, Text, Button } from "@chakra-ui/react";
import { motion } from "framer-motion";

export default function HeroSection({ onAuthOpen }) {
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 1.2 }}>
      <Box
        py={20}
        textAlign="center"
        bg="#0093d5"
        color="white"
        borderBottomRadius="2xl"
        boxShadow="lg"
      >
        <Heading fontSize={["3xl", "5xl"]} mb={4} fontWeight="extrabold">
          Smarter Surge Planning for Hospitals
        </Heading>
        <Text fontSize={["md", "2xl"]} mb={8}>
          Empowering healthcare with AI-driven, location-based readiness and resource planning.
        </Text>
        <Button colorScheme="whiteAlpha" size="lg" onClick={onAuthOpen}>
          Get Started
        </Button>
      </Box>
    </motion.div>
  );
}