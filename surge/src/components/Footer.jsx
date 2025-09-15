import { Box, Text, Flex } from "@chakra-ui/react";

export default function Footer() {
  return (
    <Box bg="#003399" py={5} mt={16}>
      <Flex justify="center">
        <Text color="white" fontSize="sm">
          &copy; {new Date().getFullYear()} Surge Planner. Inspired by WHO colors. All rights reserved.
        </Text>
      </Flex>
    </Box>
  );
}