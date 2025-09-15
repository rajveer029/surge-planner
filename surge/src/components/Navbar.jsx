import { Box, Flex, Link, Spacer, Button } from "@chakra-ui/react";

export default function Navbar({ onAuthOpen, loggedIn, setLoggedIn }) {
  return (
    <Box bg="#0093d5" px={8} py={3} boxShadow="md" position="sticky" top={0} zIndex={10}>
      <Flex align="center">
        <Box fontWeight="bold" fontSize="2xl" color="white">
          Surge Planner
        </Box>
        <Spacer />
        <Link color="white" mx={4} href="#about">
          About
        </Link>
        <Link color="white" mx={4} href="#services">
          Services
        </Link>
        <Link color="white" mx={4} href="#benefits">
          Benefits
        </Link>
        {loggedIn ? (
          <Button
            ml={6}
            colorScheme="whiteAlpha"
            variant="outline"
            onClick={() => setLoggedIn(false)}
          >
            Logout
          </Button>
        ) : (
          <Button ml={6} colorScheme="whiteAlpha" variant="outline" onClick={onAuthOpen}>
            Login / Signup
          </Button>
        )}
      </Flex>
    </Box>
  );
}