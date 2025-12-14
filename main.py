from dotenv import load_dotenv
from graph.graph import app
load_dotenv()


if __name__ == "__main__":
    print(app.invoke(input={"question":"elon musk hangi sirketlerin basindadir?"}))