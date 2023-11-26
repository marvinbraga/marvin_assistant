# Marvin Assistant | Voice Assistant with Pygame and FastAPI
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Author](https://img.shields.io/badge/author-Marcus%20Vinicius%20Braga-blue.svg)](https://www.linkedin.com/in/marvinbraga/)
[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Poetry](https://img.shields.io/badge/Poetry-1.1.6-blue.svg)](https://python-poetry.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.0.1-orange.svg)](https://www.pygame.org/news)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.65.2-green.svg)](https://fastapi.tiangolo.com/)
[![Redis](https://img.shields.io/badge/Redis-6.2.5-red.svg)](https://redis.io/)
[![LangChain](https://img.shields.io/badge/LangChain%20Framework-latest-blue.svg)](https://github.com/langchain-ai/langchain)
[![OpenAI API](https://img.shields.io/badge/OpenAI%20API-0.28.1-orange.svg)](https://beta.openai.com/)

## Description

This project is an interactive voice assistant that allows users to interact through voice commands. The software captures the user's speech, converts it into text, sends it to the OpenAI API for processing, and then converts the response back into speech.

## Technologies Used

- **Front-End:** Pygame
- **Back-End:** FastAPI
- **Data Storage:** Redis
- **Speech-to-Text and Text-to-Speech Conversion:** Specific libraries (e.g., Whisper for transcription and gTTS for speech synthesis)
- **Integration with OpenAI API**

## Environment Setup

### Prerequisites

- Python 3.10 or higher
- Poetry (Python package manager)

### Installation

To set up the development environment, follow these steps:

1. Clone the repository:
   ```
   git clone [Repository URL]
   ```
2. Install dependencies:
   ```
   poetry install
   ```

### Execution

To run the application, use the following command in the terminal:

```
python main.py
```

## Features

- **Audio Capture:** Start audio recording by clicking a button in the user interface.
- **Audio-to-Text Transcription:** The captured audio is converted into text.
- **Interaction with the OpenAI API:** The text is sent to the OpenAI API and processed.
- **Text-to-Speech Conversion:** The generated response is converted into speech.
- **Chat Interface:** Display of back-and-forth messages as a chat.

## Contribution

Contributions to the project are welcome. If you have a suggestion that would improve this, fork the repository and create a pull request. You can also simply open an issue with the "enhancement" tag. Don't forget to star the project! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the **GNU General Public License v3.0**. See `LICENSE` for more information.

## Contact

Marcus Vinicius Braga - [mvbraga@gmail.com](mailto:mvbraga@gmail.com)

Project Link: [https://github.com/marvinbraga/marvin_assistant](https://github.com/marvinbraga/marvin_assistant)
