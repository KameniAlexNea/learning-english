# English Learning Tool

This project is a web-based English learning tool that allows users to improve their writing skills by engaging in discussions on suggested topics. The tool provides feedback on user input in terms of clarity, grammar, and adherence to the topic. Additionally, it can suggest answers to topics, helping users to learn through examples.

## Features

- **Topic Suggestion**: Automatically generates a writing topic with a brief commentary to guide users.
- **User Input Evaluation**: Evaluates user responses for clarity, grammar, and relevance to the topic, offering suggestions for improvement.
- **Suggested Answers**: Provides suggested answers to the current topic to help users learn through examples.
- **Topic Refresh**: Allows users to request a new topic for discussion.

## Project Structure

```
.
├── backend/
│   ├── main.py            # FastAPI backend server
│   └── .env               # Environment variables including OpenAI API key
├── frontend/
│   └── frontend.py        # Streamlit frontend interface
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

## Installation

### Prerequisites

- Python 3.7+
- pip (Python package installer)

### Clone the Repository

```bash
git clone https://github.com/KameniAlexNea/english-learning-tool.git
cd english-learning-tool
```

### Set Up the Environment

1. **Create a Virtual Environment** (Optional but recommended):

   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```
2. **Install the Required Packages**:

   ```bash
   pip install -r requirements.txt
   ```
3. **Set Up Environment Variables**:

   Create a `.env` file in the `backend/` directory with your OpenAI API key:

   ```bash
   cd backend
   touch .env
   ```

   Add the following to your `.env` file:

   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Running the Application

### Start the Backend Server

Navigate to the `backend/` directory and run the FastAPI server:

```bash
cd backend
uvicorn main:app --reload
```

The backend will start running on `http://127.0.0.1:8000`.

### Start the Frontend Interface

Open a new terminal, navigate to the `frontend/` directory, and start the Streamlit app:

```bash
cd frontend
streamlit run frontend.py
```

This will launch the frontend in your default web browser.

## Usage

1. **Topic Suggestion**:

   - Upon loading the app, a topic is suggested automatically.
   - Click "Suggest New Topic" to receive a different topic.
2. **Writing Your Response**:

   - Type your response to the suggested topic in the provided text area.
   - Click "Evaluate" to receive feedback on your writing.
3. **Suggesting an Answer**:

   - Click "Suggest an Answer" to generate an example response based on the current topic.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## Contact

For questions or feedback, please reach out to [...].
