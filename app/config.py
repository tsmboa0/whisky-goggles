from dotenv import load_dotenv
import os

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME")
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER")
