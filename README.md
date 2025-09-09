# 4chan-toxicity-analysis


```markdown
# Toxicity Detection & Comparative Analysis

This project evaluates **toxic content detection** using two APIs:  
- 🟢 **OpenAI Moderation API**  
- 🔵 **Google Perspective API**

It collects data, runs both APIs, and performs comparative analysis to study their agreement, sensitivity, and differences.
 
---


## 📂 Project Structure


.
├── main.py # Collect posts + run toxicity detection (OpenAI & Perspective)
├── plot.py # Analysis + visualization (correlation, agreement, etc.)
├── data/ # Stores raw posts.jsonl & analyzed results.jsonl
└── README.md # Project documentation


---
````
## 🚀 Setup & Installation

1. Clone the repo:
   ```bash
   git clone <your_repo_url>
   cd analysis-task


2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   Example requirements:

   ```
   openai
   google-api-python-client
   pandas
   matplotlib
   seaborn
   scipy
   ```

3. Set up API keys:

   * **OpenAI**: create API key → [https://platform.openai.com](https://platform.openai.com)
   * **Perspective API**: get key → [https://perspectiveapi.com/](https://perspectiveapi.com/)

   Store them as environment variables:

   ```bash
   export OPENAI_API_KEY="your-openai-key"
   export PERSPECTIVE_API_KEY="your-perspective-key"
   ```

---

## 📊 Usage

1. **Collect posts & run analysis**

   ```bash
   python3 main.py
   ```

   → Saves raw posts in `data/posts.jsonl` and results in `data/results.jsonl`

2. **Run comparative analysis**

   ```bash
   python3 plot.py
   ```

   → Produces:

   * Correlation between APIs
   * Agreement/disagreement stats
   * Category distributions
   * Scatter plots & bar charts

---

## 🔎 Research Questions

Some key questions explored:

1. How well do the APIs agree on toxicity detection?
2. Which categories show the highest disagreement?
3. Which API is more sensitive to certain toxic content?
4. What patterns appear in false positives/negatives?

---

## 📈 Example Output

* ✅ Data loaded: (1352, 17)
* 🔗 Correlation (OpenAI violence vs Perspective toxicity): **0.337**
* ✅ Agreement between APIs: **74.33%**
* 📊 T-test between APIs:
 **p < 0.001**<img width="1200" height="500" alt="Figure_3" src="https://github.com/user-attachments/assets/d0f4b2ba-0f1d-467b-a633-78f7bf335c3c" />
<img width="700" height="500" alt="Figure_2" src="https://github.com/user-attachments/assets/2b22488d-9fbe-486a-adba-b92a96549663" />
<img width="1200" height="500" alt="Figure_1" src="https://github.com/user-attachments/assets/50456faf-3d55-484f-b033-7493b5b86f0c" />


---

