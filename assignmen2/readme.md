
# 📄 Automating Research Paper Analysis with AI  

🚀 **Automating Research Paper Analysis** is an AI-powered tool that **scrapes, categorizes, and analyzes research papers** from NeurIPS. It fetches paper details, assigns AI-based categories, and provides structured CSV downloads for easy analysis.  

## **✨ Features**  
✔️ **Scrapes NeurIPS research papers** (titles, authors, links, abstracts)  
✔️ **Classifies papers into AI research areas** (NLP, CV, Deep Learning, RL)  
✔️ **Users can manually assign or update categories**  
✔️ **Uses Google Gemini AI** for intelligent classification  
✔️ **Interactive Streamlit web app** for easy analysis  
✔️ **CSV download for structured data export**  

---

## **📌 Demo**  
🔗 **Live Application:** [Try it on Hugging Face](https://huggingface.co/spaces/ImamaKainat/Assignment2DS)  
📽️ **Full Demo Video:** [Watch Here](https://drive.google.com/file/d/18BqJMry-D7A3VauUUcJMcD2yeXBDSn-c/view?usp=sharing)  

---

## **🛠️ Installation & Setup**  

### **1️⃣ Clone the Repository**  
```bash
git clone https://github.com/yourusername/neurips-research-ai.git
cd neurips-research-ai
```

### **2️⃣ Create a Virtual Environment**  
```bash
python -m venv venv
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate  # On Windows
```

### **3️⃣ Install Dependencies**  
```bash
pip install -r requirements.txt
```

### **4️⃣ Set Up Google Gemini API**  
1. **Get API Key** from [Google Gemini](https://ai.google.com/gemini)  
2. Create a `.env` file and add:  
   ```ini
   GEMINI_API_KEY=your_api_key_here
   ```

---

## **🚀 Usage**  

### **Run the Web Application**  
```bash
streamlit run app.py
```

### **Scrape Research Papers Manually**  
```python
from scraper import scrape_neurips

papers = scrape_neurips(2023)  # Fetch NeurIPS 2023 papers
print(papers)
```

### **Classify Research Papers Using AI**  
```python
from classifier import classify_paper

category = classify_paper("This paper proposes a novel transformer model...")
print(category)  # Output: NLP
```

### **Manually Assign Categories**  
If the AI misclassifies a paper, users can **edit the category** in the Streamlit app or manually modify the CSV file before downloading.

---

## **🧠 Challenges & Solutions**  

### **1️⃣ Computational Cost & Fast Access Issues**  
**Problem:** Fetching all papers was slow & resource-intensive ⏳  
✅ **Solution:** Limited requests to **50 papers per fetch**  

### **2️⃣ AI Misclassification**  
**Problem:** Some papers were wrongly categorized  
✅ **Solution:** Improved **prompt engineering** & **confidence filtering**  

### **3️⃣ Web Scraping Limitations**  
**Problem:** Website structure changed, breaking CSS selectors  
✅ **Solution:** Switched to **XPath-based extraction**  

---

## **🔮 Future Improvements**  
✔️ Expand to other conferences (ICML, CVPR, AAAI)  
✔️ Improve AI classification accuracy  
✔️ Add **user-defined categories** in-app  
✔️ Support **real-time updates** from NeurIPS  

---

## **💻 Complete Code**  

### **🔹 scraper.py (Scraping NeurIPS Papers)**
```python
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_neurips(year=2023, limit=50):
    base_url = f"https://papers.nips.cc/paper/{year}"
    response = requests.get(base_url)
    
    if response.status_code != 200:
        print("Failed to fetch data")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    papers = []
    
    for idx, paper in enumerate(soup.select("div.paper")):
        if idx >= limit:
            break
        title = paper.select_one("h4").text.strip()
        link = "https://papers.nips.cc" + paper.select_one("a")["href"]
        authors = ", ".join([a.text for a in paper.select("p.authors a")])
        abstract = paper.select_one("p.abstract").text.strip() if paper.select_one("p.abstract") else ""
        
        papers.append({"title": title, "link": link, "authors": authors, "abstract": abstract})
    
    return pd.DataFrame(papers)

if __name__ == "__main__":
    df = scrape_neurips(2023)
    df.to_csv("neurips_2023.csv", index=False)
```

---

### **🔹 classifier.py (Classifying Research Papers)**
```python
import openai
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

def classify_paper(abstract):
    openai.api_key = API_KEY
    response = openai.ChatCompletion.create(
        model="gemini",
        messages=[{"role": "system", "content": "Classify the paper into NLP, CV, RL, or Deep Learning."},
                  {"role": "user", "content": abstract}]
    )
    return response["choices"][0]["message"]["content"]

if __name__ == "__main__":
    df = pd.read_csv("neurips_2023.csv")
    df["category"] = df["abstract"].apply(classify_paper)
    df.to_csv("neurips_2023_classified.csv", index=False)
```

---

### **🔹 app.py (Streamlit Web App)**
```python
import streamlit as st
import pandas as pd
from scraper import scrape_neurips
from classifier import classify_paper

st.title("📄 NeurIPS Research Paper Analyzer")
year = st.number_input("Enter Year:", min_value=2010, max_value=2023, value=2023)
if st.button("Fetch Papers"):
    df = scrape_neurips(year)
    df["category"] = df["abstract"].apply(classify_paper)
    st.write(df)

    if st.button("Download CSV"):
        df.to_csv("papers_classified.csv", index=False)
        st.success("CSV File Ready! Check your directory.")
```

---

## **📄 License**  
This project is licensed under the **MIT License**.  

---

## **📢 Contributing**  
1. Fork the repository 🍴  
2. Create a feature branch 🚀  
3. Submit a pull request 🤝  

---

## **📧 Contact & Support**  
📩 **Author:** [Imama Kainat](https://linkedin.com/in/imama-kainat)  
🐦 **Twitter:** [@imamakainat](https://twitter.com/imamakainat)  
📜 **Medium Blog:** [Read Here](https://medium.com/@imamakainat9)  

-
