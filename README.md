<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#technology-used">Technology used</a>      
    </li>
    <li><a href="#getting-started">Getting started</a></li>
    <li><a href="#file-contents-of-folder">File Contents of folder</a></li>
    <li><a href="#learn-more">Learn More</a></li>
    <li><a href="#references">References</a></li>
  </ol>
</details>
<br />
<div align="center">
  <a href="https://github.com/gdcho/vc_aggregator">
    <img src="/img/vca.png" alt="Logo" width="300" height="300">
  </a>

  <h3 align="center">Video Content Aggregator</h3>


  <p align="center">
    Video Content Generator with YouTube API, OpenAI API, and MoviePy. Create dynamic video content with a vc aggregator.
    <br />
    <a href="https://github.com/gdcho/vc_aggregator"><strong>Explore the docs »</strong></a>
    <br />
    <br />  
    <a href="https://www.youtube.com/@QuickUniqueFacts">View Clips</a>
    ·
    <a href="https://github.com/gdcho/vc_aggregator/issues">Report Bug</a>
    ·
    <a href="https://github.com/gdcho/vc_aggregator/issues">Request Feature</a>
  </p>
</div>


## Technology used

![Python Badge](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff&style=for-the-badge)
![OpenAI API](https://img.shields.io/badge/OpenAI%20API-00A67E?style=for-the-badge&logo=openai&logoColor=white)
![YouTube API](https://img.shields.io/badge/YouTube%20API-FF0000?style=for-the-badge&logo=youtube&logoColor=white)
![Pexel API](https://img.shields.io/badge/Pexel%20API-05A081?style=for-the-badge&logo=pexels&logoColor=white)
![Google Cloud Platform](https://img.shields.io/badge/Google%20Cloud%20Platform-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)
![MoviePy](https://img.shields.io/badge/MoviePy-000000?style=for-the-badge&logo=python&logoColor=white)
![FFmpeg](https://img.shields.io/badge/FFmpeg-007ACC?style=for-the-badge&logo=ffmpeg&logoColor=white)
![opencv](https://img.shields.io/badge/opencv-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![Google Auth](https://img.shields.io/badge/Google%20Auth-4285F4?style=for-the-badge&logo=google&logoColor=white)


## Getting Started

1. Clone the repo
   ```sh
   git clone https://github.com/gdcho/algo_v
   ```
2. Obtain API keys from [YouTube](https://developers.google.com/youtube/v3/getting-started), [OpenAI](https://beta.openai.com/), and [Pexels](https://www.pexels.com/api/new/) and save them in .env file
3. Install Python requirements

   ```sh
   pip install -r requirements.txt
   ```
4. Obtain OAuth Client Secret from [Google Cloud Platform](https://console.cloud.google.com/apis/credentials) and create yt_client_secret.json
5. Run the python script

   ```sh
    python3 main.py
    ```

## File Contents of folder

```
📦
├── README.md
├── __pycache__
│   ├── aggregate_fv2.cpython-311.pyc
│   └── upload_yt.cpython-311.pyc
├── aggregate_fv2.py
├── environment_variables.py
├── img
│   ├── logo.png
│   └── vca.png
├── main.py
├── output_folder
├── requirements.txt
├── test_api
│   ├── gpt_prompt.py
│   └── youtube_video_data.py
├── test_script
│   └── test_aggregate.py
├── upload_yt.py
└── yt_client_secret.json
```

## Learn More

To learn more about Python, take a look at the following resources:

- [Python Documentation](https://www.python.org/doc/) - learn about Python features and API.
- [Python Tutorial](https://docs.python.org/3/tutorial/) - an interactive Python tutorial.

To learn more about MoviePy, take a look at the following resources:

- [MoviePy Documentation](https://zulko.github.io/moviepy/) - learn about MoviePy features and API.
- [MoviePy Tutorial](https://zulko.github.io/moviepy/getting_started/your_first_clip.html) - an interactive MoviePy tutorial.

To learn more about the APIs, take a look at the following resources:

- [YouTube API](https://developers.google.com/youtube/v3/getting-started) - learn about YouTube API features and API.
- [OpenAI API](https://beta.openai.com/) - learn about OpenAI API features and API.
- [Pexels API](https://www.pexels.com/api/new/) - learn about Pexels API features and API.

To learn more about Google Cloud Platform, take a look at the following resources:

- [Google Cloud Platform](https://console.cloud.google.com/apis/credentials) - learn about Google Cloud Platform features and API.
- [Google Cloud Platform Documentation](https://cloud.google.com/docs) - learn about Google Cloud Platform features and API.


## References

[Python](https://www.python.org/) ·
[MoviePy](https://zulko.github.io/moviepy/) ·
[YouTube API](https://developers.google.com/youtube/v3/getting-started) ·
[OpenAI API](https://beta.openai.com/) ·
[Google Cloud Platform](https://console.cloud.google.com/apis/credentials) ·
[Pexels API](https://www.pexels.com/api/new/) 