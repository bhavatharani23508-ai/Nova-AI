# Nova AI

Nova AI is a Streamlit-based intelligent assistant that combines Hugging Face AI with the Open-Meteo Weather API. It automatically detects weather-related queries and provides real-time weather information, while general questions are handled by the AI assistant.

## Features

* AI-powered chat assistant
* Real-time weather information
* Automatic weather query detection
* City-based weather search
* Temperature, humidity, and wind speed
* Session-based chat history
* Secure environment variable configuration
* Simple and responsive interface

## Technologies

* Python
* Streamlit
* Hugging Face Inference API
* Open-Meteo API
* Requests
* python-dotenv

## How It Works

Nova analyzes the user's query and determines whether it is a weather-related request. Weather queries are processed through the Open-Meteo API, while general queries are sent to the Hugging Face AI model.

## Example Queries

```text
What is Artificial Intelligence?
Explain Python functions.
What's the weather in Chennai?
Temperature in Mumbai
Weather in Coimbatore
Forecast for Bangalore
```

## Installation

```bash
git clone <your-repository-url>
cd Nova-AI
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file and add:

```env
HF_TOKEN=your_huggingface_access_token
```

Run the application:

```bash
python -m streamlit run app.py
```

## Security

API credentials are stored using environment variables and should not be committed to GitHub. The `.env` file is excluded through `.gitignore`.

## Future Enhancements

* Multi-day weather forecasts
* Rain probability
* Improved natural-language query detection
* Weather visualizations
* Voice interaction
* Streamlit Cloud deployment

## Author

Bhavatharani
