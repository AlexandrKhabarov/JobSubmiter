from app.base import init
from config.config import Mode

app = init(Mode.DEVELOPMENT)

if __name__ == "__main__":
    app.run()
