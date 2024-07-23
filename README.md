# Information Sheet

## Title: New York Times Article Corpus (possible year range: 1851 - yesterday)

**Description**:
This repository contains scripts to scrape a corpus of articles from "The New York Times Developer Network". Possible year ranges are from 1851 to yesterday, and the code extracts articles for every month in each year. It is intended for research and analysis purposes, providing a comprehensive snapshot of NYT content for the desired period. 
- *Note*: Due to the NYT Terms of Service, full-text articles are unavailable and so only snippets, lead paragraphs, and titles can be scraped (as of 23/07/2024).
- *Note*: This is the order of scripts to run to compile your own NYT corpus:
    1)  "data_downloading.ipynb"
        - *Aim*: This script retrieves article data from the NYT archive API for a user specified year range and saves it to a file of each month's data before concatenating all individual files into a single CSV file.
        - *Note*: You must have the "get_corpus.py" file in our repo for this script to run.
    3)  "corpus_descriptives.ipynb"
        - *Aim*: This script retrieves article data from the NYT archive API for a user specified year range and saves it to a file of each month's data before concatenating all individual files into a single CSV file.

## Data Collection Methodology

- **Source**: The New York Times Developer Network
- **Time Frame**: January 1851 - yesterday
- **API Endpoint**: `https://api.nytimes.com/svc/archive/v1/{year}/{month}.json?api-key={key}`
- **Parameters Used**: API key for authentication

## Data Structure 
- *Note*: Information pertains to the "nyt_corpus.csv" dataset that scripts compile. You may wish to include other metadata.

- **Format**: JSON
- **Columns**: `['title', 'section_name', 'snippet', 'lead_paragraph', 'year', 'month', 'web_url']`
- **Schema**:
  - `title`: Title of the article
  - `section_name`: Section of the newspaper (e.g., World, Business)
  - `snippet`: Snapshot of the article
  - `lead_paragraph`: Leading paragraph of the article
  - `year`: Year in which the article was published
  - `month`: Month in which the article was published
  - `web_url`: Article URL

## Data Volume 
- *Note*: Information pertains to the final cleaned "nyt_corpus.csv" dataset that we compiled within the specified year range.

- **Year Range**: 01/1930 - 12/2023
  - Unique values for year: 94; unique values for month: 12
- **Total Articles**: 10,891,026
- **Total Size**: 4,062,237 KB
- **Section Types**: 91 (some may be duplicates due to incorrect parsing, e.g., 'Archives', '|Archives')

## Usage and Licensing

- **Permissions**: Users must comply with the New York Times API terms of service. Scripts can be downloaded and used under the Creative Commons Attribution 4.0 International License, which "requires that users give appropriate credit, provide a link to the license, and indicate if changes were made. It allows for both commercial and non-commercial use of the work, as long as attribution is provided. This is in line with the general requirement for attribution in the Creative Commons Attribution (CC BY) licenses."
- **Attribution**: Please credit the New York Times as the data source, and this GitHub repository if you re-use the scripts.

## Data Quality and Limitations

- **Quality Control**: Articles have been cleaned to remove duplicates and incomplete entries.
- **Known Limitations**: The corpus may contain biases inherent to the New York Times' reporting. Additionally, as full-text articles are not available, tokens are limited, affecting the comprehensiveness of the dataset.

## Contact Information

- **Compiled by**: Hugo Lyons Keenan & Naomi Baes
- **Email**: [your-email@example.com](mailto:your-email@example.com)
- **Support**: For questions, please contact [your-email@example.com](mailto:your-email@example.com).

# Data Statement

### Purpose:
This data statement provides a comprehensive overview of the New York Times Article Corpus, which has been compiled for research and analysis purposes. The corpus aims to facilitate studies in various fields, including but not limited to, journalism, data science, natural language processing, and historical research.

### Scope:
- **Content**: Articles from the New York Times spanning from January 1930 to December 2023.
- **Data Points**: Title, section name, snippet, lead paragraph, year, month, and web URL of each article.

### Methodology:
- Data was collected using the New York Times API, specifically from the endpoint `https://api.nytimes.com/svc/archive/v1/{year}/{month}.json`.
- Only metadata and article snippets are included due to API restrictions and terms of service.

### Usage:
- **Research and Analysis**: This corpus can be used for text analysis, trend identification, and other research purposes.
- **Education**: Suitable for educational purposes to demonstrate data scraping, cleaning, and analysis techniques.
- **Development**: Can be utilized in developing machine learning models and natural language processing applications.

### Quality and Limitations:
- **Quality Control**:
  - The dataset has undergone cleaning to remedy 116,799 malformed rows and rows where the number of columns did not match the header. Additionally, 79 rows were removed where the year did not meet the specified criteria (not a 4-digit number or not within the range 1930-2023), and rows in the year 1851 were also removed.
- **Limitations**:
  - The corpus may reflect biases inherent in the New York Times' reporting.
  - Full-text articles are not available, which may limit the depth of certain analyses.
  - The data is as comprehensive as allowed by the API restrictions, focusing on snippets, lead paragraphs, and titles.
- **NA counts for each column in the final cleaned data frame - "nyt_corpus_cleaned.csv"**:
  - Number of NA values, total rows, and percentage of NA values in each column:
  - Column 0: NA Count = 615, Total Rows = 10891026, Percentage = 0.01%
  - Column 1: NA Count = 2295, Total Rows = 10891026, Percentage = 0.02%
  - Column 2: NA Count = 4494865, Total Rows = 10891026, Percentage = 41.27%
  - Column 3: NA Count = 5979376, Total Rows = 10891026, Percentage = 54.90%
  - Column 4: NA Count = 0, Total Rows = 10891026, Percentage = 0.00%
  - Column 5: NA Count = 0, Total Rows = 10891026, Percentage = 0.00%
  - Column 6: NA Count = 0, Total Rows = 10891026, Percentage = 0.00% 

### Ethical Considerations:
- Users must comply with the New York Times API terms of service and ensure proper attribution: [NYT API Terms](https://developer.nytimes.com/terms).
- Consider the ethical implications of the data usage, especially regarding the representation of sensitive topics and historical contexts.

### Acknowledgements: 
- Code for some scripts were inspired from Salvatore Giorgi's repository: https://osf.io/uya29/

### Contact:
- **Compiled by**: Hugo Lyons Keenan & Naomi Baes
- **Emails**: [your-email@example.com](mailto:your-email@example.com) & [naomi_baes@hotmail.com](mailto:naomi_baes@hotmail.com)
- **Support**: For questions, please contact [your-email@example.com](mailto:your-email@example.com).

### Citation:
Please cite this corpus as follows:
Hugo Lyons Keenan & Naomi Baes. "New York Times Article Corpus (1930-2023)." Retrieved from [https://github.com/naomibaes/NYT].
