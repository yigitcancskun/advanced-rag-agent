# Advanced RAG (Retrieval-Augmented Generation) System

Bu proje, LangChain ve LangGraph kullanarak gelişmiş bir RAG sistemi oluşturmayı amaçlamaktadır. Sistem, kullanıcı sorularını analiz ederek ya veritabanından ya da web aramasından bilgi çekerek cevap üretir.

## Proje Yapisi

```
advancedrag/
├── main.py                     # Ana uygulama dosyasi
├── ingestion.py                # Veri yukleme ve ChromaDB entegrasyonu
├── requirements.txt            # Proje bagimliliklari
├── .env                        # API anahtarlari (gitignore'da)
├── .gitignore                  # Git ignore dosyasi
├── chroma_db/                  # ChromaDB veritabani (gitignore'da)
└── graph/
    ├── __init__.py
    ├── state.py                # Graph state tanimlari
    ├── node_constants.py       # Node sabitleri
    ├── graph.py                # LangGraph workflow tanimlari
    ├── chains/
    │   ├── __init__.py
    │   ├── router.py           # Soru yonlendirme chain'i
    │   ├── generation.py       # Cevap uretme chain'i
    │   ├── retrieval_grader.py # Dokuman alakalilik degerlendirme
    │   ├── hallucination_grader.py # Halusinasyon kontrolu
    │   └── answer_grader.py    # Cevap kalite degerlendirme
    └── nodes/
        ├── __init__.py
        ├── retrieve.py         # Vectorstore'dan veri cekme
        ├── generate.py         # LLM ile cevap uretme
        ├── grade_documents.py  # Dokuman degerlendirme
        └── web_search.py       # Web aramasi (DuckDuckGo)
```

## Kurulum

### 1. Gerekli paketleri yukleyin

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install duckduckgo-search ddgs
```

### 2. .env dosyasi olusturun

```
OPENAI_API_KEY=your_api_key_here
```

### 3. Uygulamayi calistirin

```bash
python main.py
```

## Yapilan Adimlar

### 1. Proje Yapisinin Olusturulmasi

- `venv` sanal ortami olusturuldu ve aktive edildi
- `requirements.txt` dosyasi olusturuldu ve gerekli paketler eklendi
- `.env` ve `.gitignore` dosyalari olusturuldu

### 2. Veri Yukleme (Ingestion)

- `ingestion.py` dosyasi olusturuldu
- Web sayfasindan icerik cekmek icin `WebBaseLoader` kullanildi
- Metin parcalama icin `RecursiveCharacterTextSplitter` kullanildi
- `ChromaDB` vector veritabanina embedding'ler kaydedildi
- `OpenAIEmbeddings` ile vektorlestirme yapildi

### 3. Graph State Tanimlari

- `graph/state.py` dosyasi olusturuldu
- `GraphState` TypedDict tanimi yapildi (question, generation, web_search, documents)

### 4. Router Chain Olusturma

- `graph/chains/router.py` dosyasi olusturuldu
- `RouteQuery` Pydantic modeli tanimlandi (vectorstore veya websearch)
- Kullanici sorusunu analiz edip yonlendiren chain olusturuldu

### 5. Generation Chain Olusturma

- `graph/chains/generation.py` dosyasi olusturuldu
- `ChatPromptTemplate` ile prompt tanimlandi
- `StrOutputParser` ile cikti parse edildi

### 6. Retrieval Grader Olusturma

- `graph/chains/retrieval_grader.py` dosyasi olusturuldu
- `GradeDocuments` Pydantic modeli tanimlandi
- Dokumanlarin soruyla alakali olup olmadigini degerlendiren chain olusturuldu

### 7. Hallucination Grader Olusturma

- `graph/chains/hallucination_grader.py` dosyasi olusturuldu
- `GradeHallucinations` Pydantic modeli tanimlandi
- Uretilen cevabin gerceklere dayanip dayanmadigini kontrol eden chain olusturuldu

### 8. Answer Grader Olusturma

- `graph/chains/answer_grader.py` dosyasi olusturuldu
- `GradeAnswer` Pydantic modeli tanimlandi
- Cevabin soruyu adresleyip adreslemedigini degerlendiren chain olusturuldu

### 9. Node Fonksiyonlari Olusturma

- `graph/nodes/retrieve.py` - Vectorstore'dan dokuman cekme
- `graph/nodes/generate.py` - LLM ile cevap uretme
- `graph/nodes/grade_documents.py` - Dokumanlari degerlendirme ve filtreleme
- `graph/nodes/web_search.py` - DuckDuckGo ile web aramasi (Tavily yerine ucretsiz alternatif)

### 10. LangGraph Workflow Olusturma

- `graph/graph.py` dosyasi olusturuldu
- `StateGraph` ile workflow tanimlandi
- Conditional entry point ile soru yonlendirme eklendi
- Node'lar arasi edge'ler tanimlandi
- Hallucination ve answer grading ile kalite kontrolu eklendi

### 11. Web Search Entegrasyonu

- Tavily yerine DuckDuckGo kullanildi (ucretsiz, API key gerektirmez)
- `langchain_community.tools.DuckDuckGoSearchResults` kullanildi

## Kullanilan Teknolojiler

- **Python 3.12**
- **LangChain** - LLM orkestrasyon
- **LangGraph** - State machine workflow
- **ChromaDB** - Vector veritabani
- **OpenAI GPT** - Dil modeli
- **DuckDuckGo** - Web aramasi
- **Pydantic** - Veri validasyonu

## Workflow Akisi

```
                    +------------------+
                    |   User Question  |
                    +--------+---------+
                             |
                    +--------v---------+
                    |   Route Question |
                    +--------+---------+
                             |
              +--------------+--------------+
              |                             |
     +--------v--------+           +--------v--------+
     |   Vectorstore   |           |   Web Search    |
     +--------+--------+           +--------+--------+
              |                             |
     +--------v--------+                    |
     | Grade Documents |                    |
     +--------+--------+                    |
              |                             |
              +-------------+---------------+
                            |
                   +--------v--------+
                   |    Generate     |
                   +--------+--------+
                            |
                   +--------v--------+
                   | Check Hallucin. |
                   +--------+--------+
                            |
                   +--------v--------+
                   |  Grade Answer   |
                   +--------+--------+
                            |
                   +--------v--------+
                   |     Output      |
                   +-----------------+
```

## Ornek Kullanim

```python
from graph.graph import app

result = app.invoke(input={"question": "What is AI agent?"})
print(result)
```

## Notlar

- `.env` dosyasinda `OPENAI_API_KEY` tanimlanmis olmalidir
- ChromaDB veritabani `chroma_db/` klasorunde saklanir
- Web aramasi icin internet baglantisi gereklidir

---

Bu proje, Atil Samancioglu'nun "Yapay Zeka Uygulamalari: Langchain, RAG, LLM Orchestration" kursundan alinmistir.
