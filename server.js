const express = require('express');
const bodyParser = require('body-parser');
const { Configuration, OpenAIApi } = require('openai');

const app = express();
const port = 3000;

app.use(bodyParser.json());
app.use(express.static('public')); // Serve static files from "public" directory

// Replace 'your-openai-api-key' with your actual API key
const configuration = new Configuration({
    apiKey: 'your-openai-api-key',
});

const openai = new OpenAIApi(configuration);

app.post('/ask-gpt', async (req, res) => {
    const userMessage = req.body.message;

    try {
        const completion = await openai.createCompletion({
            model: 'text-davinci-003', // Or any available GPT model
            prompt: userMessage,
            max_tokens: 150,
            temperature: 0.7,
        });

        const gptReply = completion.data.choices[0].text.trim();
        res.json({ reply: gptReply });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Something went wrong!' });
    }
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
