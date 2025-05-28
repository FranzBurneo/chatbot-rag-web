import {
  Box,
  Button,
  Flex,
  Input,
  Text,
  VStack,
  Heading,
  Spinner,
} from '@chakra-ui/react';
import { useColorModeValue } from "@/components/ui/color-mode"
import { useState, useRef, useEffect } from 'react';
import axios from 'axios';

interface Message {
  sender: 'user' | 'bot';
  text: string;
}

const ChatBot = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMessage: Message = { sender: 'user', text: input };
    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const res = await axios.post('http://192.168.0.103:8000/ask', { question: input });
      setMessages((prev) => [...prev, { sender: 'bot', text: res.data.answer }]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { sender: 'bot', text: 'Error al conectar con el servidor.' },
      ]);
    }

    setInput('');
    setLoading(false);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') sendMessage();
  };

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const userBg = useColorModeValue('blue.500', 'blue.300');
  const botBg = useColorModeValue('gray.200', 'gray.700');

  return (
    <Flex
      h="100vh"
      justify="center"
      align="center"
      bg={useColorModeValue('gray.50', 'gray.800')}
      px={4}
      p={4}
    >
      <Flex
        direction="column"
        bg={useColorModeValue('white', 'gray.900')}
        boxShadow="lg"
        borderRadius="lg"
        p={4}
        w="100%"
        maxW="800px"
        h="100%"
      >
        <Heading as="h2" size="md" textAlign="center" mb={2}>
          Asistente de Créditos
        </Heading>

        {/* Área de mensajes que se expande */}
        <Box
          flex="1"
          overflowY="auto"
          px={2}
          py={2}
          border="1px solid"
          borderColor="gray.200"
          rounded="md"
          bg={useColorModeValue('gray.100', 'gray.800')}
          mb={4}
        >
          <VStack align="stretch">
            {messages.map((msg, i) => (
              <Box
                key={i}
                alignSelf={msg.sender === 'user' ? 'flex-end' : 'flex-start'}
                bg={msg.sender === 'user' ? userBg : botBg}
                color={msg.sender === 'user' ? 'white' : 'black'}
                px={4}
                py={2}
                borderRadius="xl"
                maxW="80%"
              >
                <Text fontSize="sm">
                  <strong>{msg.sender === 'user' ? 'Tú' : 'Bot'}:</strong> {msg.text}
                </Text>
              </Box>
            ))}
            {loading && (
              <Flex align="center" gap={2}>
                <Spinner size="sm" />
                <Text fontSize="xs" color="gray.500">
                  Bot está escribiendo...
                </Text>
              </Flex>
            )}
            <div ref={scrollRef} />
          </VStack>
        </Box>

        {/* Input siempre visible abajo */}
        <Flex gap={2}>
          <Input
            placeholder="Escribe tu mensaje..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            flex={1}
          />
          <Button colorScheme="blackAlpha" onClick={sendMessage}>
            Enviar
          </Button>
        </Flex>
      </Flex>
    </Flex>
  );
};

export default ChatBot;