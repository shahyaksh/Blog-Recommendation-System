
# Blog Recommendation System

This project is a Blog Recommendation System that utilizes collaborative and content-based filtering methods to recommend blogs to users. The system is built using a Medium Web Scraper, a TechTonic API, and a database for storing blog data.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Execution Steps](#execution-steps)
- [API Documentation](#api-documentation)
- [License](#license)

## Prerequisites

- Python 3.x
- Flask
- SQL database (SQLite recommended)
- Required Python libraries (refer to `requirements.txt`)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/shahyaksh/Blog-Recommendation-System.git
   cd Blog-Recommendation-System
   ```

2. Install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```

## Execution Steps

1. **Collect Blogs**  
   Use the [Medium Web Scraper](https://github.com/shahyaksh/MediumWebscrapper) to collect blogs from Medium. Navigate to the Medium Web Scraper directory and run the following command:

   ```bash
   streamlit run app.py
   ```

2. **Create the `blog_recommendation_system` Database**  
   Run the SQL files provided in the `Complete Data` folder to create the necessary database structure and populate it with the scraped blog data.

3. **Start the TechTonic API**  
   Navigate to the TechTonic API directory and run the API on localhost:

   ```bash
   uvicorn app.main:app
   ```

4. **Start the Flask Server**  
   Finally, start the Flask server to make the project execute smoothly:

   ```bash
   python run.py
   ```

## API Documentation

For detailed API endpoints and usage instructions, please refer to the [TechTonicAPI README](https://github.com/shahyaksh/TechTonicAPI).

# Demo
Check out the demo of the full recommendation system running [here](https://drive.google.com/file/d/1gp9mbT0DiPKgu88i6PUTAf2LhLs_bRVj/view?usp=drive_link)
## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
