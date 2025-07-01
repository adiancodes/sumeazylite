<h1 align="center" id="title">SumEazy</h1>

<p align="center"><img src="https://socialify.git.ci/adiancodes/sumeazylite/image?font=JetBrains+Mono&amp;language=1&amp;name=1&amp;owner=1&amp;pattern=Solid&amp;stargazers=1&amp;theme=Dark" alt="project-image"></p>

<p id="description">Sumeazy is a Flask-based web app that allows users to summarize news articles and YouTube videos with built-in sentiment analysis. It supports both English and Hindi content and uses AssemblyAI for transcribing YouTube videos. Users can sign up log in and save summaries to view their history later. It's perfect for digesting long-form content quickly and effectively.</p>

<p align="center"><img src="https://img.shields.io/github/stars/adiancodes/sumeazylite?style=social" alt="shields"></p>

<h2> Demo</h2>



https://github.com/user-attachments/assets/eb9c48bd-fd7a-4e44-b08b-d7725594cab9



<h2>Project Screenshots:</h2>

![Screenshot 2025-07-01 195102](https://github.com/user-attachments/assets/da74b7d0-8576-4808-9361-eb36ab107b9a)

![Screenshot 2025-07-01 195330](https://github.com/user-attachments/assets/b1ffa3fc-37d0-4f80-a93f-f5b4e5146d3f)

![Screenshot 2025-07-01 195434](https://github.com/user-attachments/assets/92d34a0f-8199-4859-934a-dd34594f1a89)

![Screenshot 2025-07-01 200648](https://github.com/user-attachments/assets/d43257bf-8145-49aa-9780-560bc3fdcae6)

![Screenshot 2025-07-01 200605](https://github.com/user-attachments/assets/b693c516-a3e4-477c-a2e3-6cb388ff5bb6)


  
<h2> Features</h2>

Here're some of the project's best features:

*   Summarize any online news article
*   Extract and summarize YouTube videos using audio transcription
*   Get sentiment analysis (positive negative neutral)
*   User authentication with secure password hashing
*   Save and view summary history in your personal dashboard

<h2> Installation Steps:</h2>

<p>1. Prerequisites</p>

```
- Python 3.8+ - MongoDB instance (local or cloud via MongoDB Atlas) - AssemblyAI API key (for YouTube transcription)
```

<p>2. Clone the repo</p>

```
git clone https://github.com/adiancodes/sumeazylite.git 
```

<p>3. Go to directory</p>

```
cd sumeazylite
```

<p>4. Install dependencies</p>

```
pip install -r requirements.txt
```

<p>5. Download NLTK tokenizer data (used in summarizer.py)</p>

```
python -c "import nltk; nltk.download('punkt')"
```

<p>6. Create a .env file in the root directory and add:</p>

```
SECRET_KEY=your-secret-key
```

```
MONGO_URI=your-mongodb-uri
```

```
ASSEMBLYAI_API_KEY=your-assemblyai-api-key
```

<h2> Contribution Guidelines:</h2>

Pull requests are welcome! For major changes open an issue first to discuss what you’d like to change

  
  
<h2> Built with</h2>

Technologies used in the project:

*   Flask
*   MongoDB
*   Newspaper3k
*   AssemblyAI
*   TextBlob
*   yt-dlp
*   NLTK
*   BootStrap

<h2>🛡 License:</h2>

This project is licensed under the This project is licensed under the MIT License.

<h2>💖Like my work?</h2>

Created with ❤️ by @adiancodes
